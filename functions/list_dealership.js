/**
 * Get all dealerships
 */
const Cloudant = require('@cloudant/cloudant');

async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });

    try {
        let db = await cloudant.db.use("dealerships");
        //let allDocs = await db.list({ include_docs: true });
        
        let q = { selector: {} };
        if (params.state) {
            q = {
                selector: {
                   st: { "$eq": params.state}
                },
            };    
        }
        
        let allDocs = await db.find(q)
        
        return {
            "data": allDocs.docs,
        };
    } catch (error) {
        return { error: error.description };
    }
}