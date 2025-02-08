import { PublicKey, Connection } from "@solana/web3.js";
import * as borsh from "@project-serum/borsh";
import fetch from "node-fetch";  
import * as fs from "fs";  

const jsonString = process.argv[2];

const tokenMint = new PublicKey(jsonString);
const programId = new PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s");
const seeds = [Buffer.from("metadata"), programId.toBytes(), tokenMint.toBytes()];

const [metadataPDA, bump] = PublicKey.findProgramAddressSync(seeds, programId);
const connection = new Connection("https://api.mainnet-beta.solana.com");
const accountInfo = await connection.getAccountInfo(metadataPDA);

const borshMetadataLayout = borsh.struct([
  borsh.u8('key'),
  borsh.publicKey('updateAuthority'),
  borsh.publicKey('mint'),
  borsh.str('name'),
  borsh.str('symbol'),
  borsh.str('uri'),
]);


////////// npx esrun dec.ts

if (accountInfo) {
  const metadata = borshMetadataLayout.decode(accountInfo.data);
  const name = metadata.name.replace(/\x00+$/, '');
  const symbol = metadata.symbol.replace(/\x00+$/, '');
  const uri = metadata.uri.replace(/\x00+$/, '');

  // console.log(name);
  console.log(symbol);
  // console.log(uri);

  if (uri) {
    try {
      // grab uri json
      const response = await fetch(uri);
      if (!response.ok) {
        throw new Error(`Failed to fetch URI: ${response.statusText}`);
      }

      // // find twitter
      const metadataJson = await response.json();
      // console.log(metadataJson.twitter);
      // if (metadataJson.twitter) {
      //   console.log(metadata.twitter)
      // } else {
      //   console.log("No 'twitter found in the metadata.")
      // }

      // find image
      if (metadataJson.image) {
        const imageUrl = metadataJson.image;

        // download image
        const imageResponse = await fetch(imageUrl);
        if (!imageResponse.ok) {
          throw new Error(`Failed to download image: ${imageResponse.statusText}`);
        }

        // extract image
        const imageBuffer = await imageResponse.buffer();
        fs.writeFileSync(`src/data/icon.jpg`, imageBuffer);
      } else {
        console.error("image not found in the metadata.");
      }
    } catch (error) {
      console.error("Error fetching or processing metadata:", error);
    }
    
  }
  // const metadataObject = {
  //   name: name || null,
  //   symbol: symbol || null,
  // };

  // Step 2: Write the object to a JSON file
  // fs.writeFileSync('data/metadata.json', JSON.stringify(metadataObject, null, 2));
  // console.log("Metadata has been written to metadata.json");
}
 