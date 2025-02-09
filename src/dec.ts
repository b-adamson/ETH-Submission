import { PublicKey, Connection } from "@solana/web3.js";
import * as borsh from "@project-serum/borsh";
import fetch from "node-fetch";  
import * as fs from "fs";  

const jsonString = process.argv[2];
let tokenMint;
let imagedir = "data/default.png";

try {
  tokenMint = new PublicKey(jsonString);
} catch (error) {
  throw new Error("invalid key");
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
          imagedir = "data/logo.png"
          await downloadImage(imageUrl);
        }
      } catch (error) {

      }
    }

    const metadataObject = {
      name: name || null,
      symbol: symbol || null,
      image: imagedir,
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
    console.log(2);
    const imageBuffer = await imageResponse.buffer();
    fs.writeFileSync('frontend/data/logo.png', imageBuffer);
  } catch (error) {
    console.error("Error downloading image:", error);
  }
}

fetchMetadata();
