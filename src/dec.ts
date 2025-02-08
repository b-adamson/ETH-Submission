import { PublicKey, Connection } from "@solana/web3.js";
import * as borsh from "@project-serum/borsh";
import fetch from "node-fetch";  
import * as fs from "fs";  
import path from "path"; 

const jsonString = process.argv[2];
const tokenMint = new PublicKey(jsonString);
const programId = new PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s");
const seeds = [Buffer.from("metadata"), programId.toBytes(), tokenMint.toBytes()];

const [metadataPDA, bump] = PublicKey.findProgramAddressSync(seeds, programId);
const connection = new Connection("https://api.mainnet-beta.solana.com");

function copyDefaultIcon() {
  const defaultIconPath = path.join(__dirname, 'src/data/defaulticon.jpg');
  const targetPath = path.join(__dirname, 'src/data/icon.jpg');

  try {
    if (fs.existsSync(defaultIconPath)) {
      fs.copyFileSync(defaultIconPath, targetPath);
      console.error("Default icon copied as icon.jpg.");
    } else {
      console.error("Default icon not found.");
    }
  } catch (error) {
    console.error("Error copying default icon:", error);
  }
}

async function fetchMetadata() {
  try {
    const accountInfo = await connection.getAccountInfo(metadataPDA);
    
    if (!accountInfo) {
      throw new Error("Account info not found.");
    }

    const borshMetadataLayout = borsh.struct([
      borsh.u8('key'),
      borsh.publicKey('updateAuthority'),
      borsh.publicKey('mint'),
      borsh.str('name'),
      borsh.str('symbol'),
      borsh.str('uri'),
    ]);

    const metadata = borshMetadataLayout.decode(accountInfo.data);
    const name = metadata.name.replace(/\x00+$/, '');
    const symbol = metadata.symbol.replace(/\x00+$/, '');
    const uri = metadata.uri.replace(/\x00+$/, '');
    let twitter = null;
    let imageUrl = null;

    // Log only the symbol to stdout
    console.log(symbol);

    if (uri) {
      try {
        const response = await fetch(uri);
        if (!response.ok) {
          throw new Error(`Failed to fetch URI: ${response.statusText}`);
        }

        const metadataJson = await response.json();
        twitter = metadataJson.twitter || null;
        imageUrl = metadataJson.image || null;

        // Download image if found
        if (imageUrl) {
          const imageResponse = await fetch(imageUrl);
          if (!imageResponse.ok) {
            copyDefaultIcon()
          }

          const imageBuffer = await imageResponse.buffer();
          if (!fs.existsSync('src/data')) {
            fs.mkdirSync('src/data', { recursive: true });
          }
          fs.writeFileSync('src/data/icon.jpg', imageBuffer);
        } else {
          copyDefaultIcon()
        }
      } catch (error) {
        copyDefaultIcon()
      }
    }

    // Create and write metadata object to JSON file
    const metadataObject = {
      name: name || null,
      symbol: symbol || null,
      twitter: twitter,
    };

    fs.writeFileSync('src/data/metadata.json', JSON.stringify(metadataObject, null, 2));

  } catch (error) {
    console.error("Error fetching account information or processing metadata:", error);
  }
}

// Run the function
fetchMetadata();