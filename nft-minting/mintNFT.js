require('dotenv').config({path: __dirname + '/.env.node'});
const xrpl = require('xrpl')
const { encodeReportDataToURI } = require('./nftURI'); // Import the encodeReportDataToURI function

const walletSecret = process.env.WALLET_SECRET; // Accessing the wallet secret from environment variables
const xrplWsUrl = process.env.XRPL_WS_URL; // Accessing the XRPL WebSocket URL from environment variables


/* // Parse command-line argument as JSON
const jsonData = process.argv[2] ? JSON.parse(process.argv[2]) : null;

if (!jsonData) {
  console.error("No JSON data provided.");
  process.exit(1);
}
*/

async function checkTransactionStatus(client, txHash) {
    try {
        const tx = await client.request({
            command: 'tx',
            transaction: txHash
        });
        console.log("Transaction status:", tx);
    } catch (error) {
        console.error("Error fetching transaction status:", error);
    }
}

async function mintToken(wallet, client, uri) {
    const currentLedgerVersion = await client.getLedgerIndex()
    const lastLedgerSequence = currentLedgerVersion + 10; // Adding a buffer

    const transactionJson = {
        TransactionType: "NFTokenMint",
        Account: wallet.classicAddress,
        URI: uri, // Use the dynamically generated URI
        Flags: 11, // Combined flags value: tfBurnable, tfOnlyXRP, tfTransferable,
        TransferFee: 0,
        NFTokenTaxon: 0, // Required, but if you have no use for it, set to zero.
        LastLedgerSequence: lastLedgerSequence
    }

    const prepared = await client.autofill(transactionJson)
    const signed = wallet.sign(prepared)
    
    // Ensure txResponse is defined here by awaiting the submitAndWait call
    try {
        const txResponse = await client.submitAndWait(signed.tx_blob);
        console.log("Transaction hash:", txResponse.result.hash);

        // After successfully submitting, check and log the transaction status
        await checkTransactionStatus(client, txResponse.result.hash);
    } catch (error) {
        console.error("Error during transaction submission:", error);
    }
}

    async function main() {
    const client = new xrpl.Client(xrplWsUrl)
    await client.connect()

    const wallet = xrpl.Wallet.fromSeed(walletSecret)
    console.log(`Using address ${wallet.classicAddress}`)

    // Example report data
    const jsonData = {
        farmerId: "FARM12345",
        location: "Location A",
        livestockCount: 100,
        milkProduction: 5000, // liters per day
        feedConsumption: { corn: 1000, soybean: 500 }, // kg per day
        methaneEmissions: 200 // kg per day
    };

    // Generate the URI from the report data
    const uri = encodeReportDataToURI(jsonData)

    await mintToken(wallet, client, uri)

    await client.disconnect()
    }

main().catch(console.error)
