import { PublicKey, Connection } from "@solana/web3.js";
import * as borsh from "@project-serum/borsh";
import fetch from "node-fetch";  
import * as fs from "fs";  
import path from "path"; 

// if (fs.existsSync('src/data/metadata.json')) {fs.unlinkSync('src/data/metadata.json');}

const jsonString = process.argv[2];
let tokenMint;
try {
  tokenMint = new PublicKey(jsonString);
} catch (error) {
  throw new Error("invalid key"); // empty address
}
const programId = new PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s");
const seeds = [Buffer.from("metadata"), programId.toBytes(), tokenMint.toBytes()];

const [metadataPDA, bump] = PublicKey.findProgramAddressSync(seeds, programId);
const connection = new Connection("https://api.mainnet-beta.solana.com");

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

    console.log(symbol); // Log symbol

    if (uri) {
      try {
        const response = await fetch(uri);
        if (!response.ok) {
          throw new Error(`Failed to fetch URI: ${response.statusText}`);
        }

        const metadataJson = await response.json();
        twitter = metadataJson.twitter || null;
        imageUrl = metadataJson.image || null;

        if (imageUrl) {
          await downloadImage(imageUrl);
        } else {
          await downloadImage("https://dhw7e56xnudlkirsdiylutupx6x2e67l5pejkbjxu65f5mjoqi7q.arweave.net/Ge3yd9dtBrUiMhowuk6Pv6-ie-vryJUFN6e6XrEugj8?ext=png");
        }
      } catch (error) {
        await downloadImage("https://dhw7e56xnudlkirsdiylutupx6x2e67l5pejkbjxu65f5mjoqi7q.arweave.net/Ge3yd9dtBrUiMhowuk6Pv6-ie-vryJUFN6e6XrEugj8?ext=png");
      }
    }

    const metadataObject = {
      name: name || null,
      symbol: symbol || null,
      image: "data/logo.png",
      twitter: twitter
    };

    const metadataArray = [metadataObject];

    fs.writeFileSync('src/data/metadata.json', JSON.stringify(metadataArray, null, 2));

  } catch (error) {
    console.error("Error fetching account information or processing metadata:", error);
  }
}

async function downloadImage(url) {
  try {
    const imageResponse = await fetch(url);
    if (!imageResponse.ok) {
      throw new Error("Failed to fetch image.");
    }

    const imageBuffer = await imageResponse.buffer();
    if (!fs.existsSync('src/data')) {
      fs.mkdirSync('src/data', { recursive: true });
    }
    fs.writeFileSync('frontend/data/logo.png', imageBuffer);
  } catch (error) {
    console.error("Error downloading image:", error);
  }
}

// Run the function
fetchMetadata();
