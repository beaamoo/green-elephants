const xrpl = require('xrpl');

function optimizeAndEncodeReportData(reportData) {
    // Example optimization: Shorten property names
    const optimizedData = {
        fid: reportData.farmerId,
        loc: reportData.location,
        lc: reportData.livestockCount,
        mp: reportData.milkProduction,
        fc: reportData.feedConsumption, // Consider further optimization here
        me: reportData.methaneEmissions
    };

    // Serialize and Base64 encode
    const jsonData = JSON.stringify(optimizedData);
    const base64Data = Buffer.from(jsonData).toString('base64');

    // Construct data URI with Base64 encoded data
    const dataUri = `data:application/json;base64,${base64Data}`;

    // Convert to hexadecimal format for XRPL
    const hexUri = xrpl.convertStringToHex(dataUri);

    // Check final size
    if (hexUri.length > 512) { // 256 bytes * 2 characters per byte
        throw new Error('The final URI exceeds 256 bytes after encoding.');
    }

    return hexUri;
}

// Export adjusted function
module.exports = { encodeReportDataToURI: optimizeAndEncodeReportData };

