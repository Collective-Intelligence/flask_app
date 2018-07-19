/**
 *  Super simple client app just to test things
 *  @author Una Ada (Trewbot) <una@phene.co>
 */
const
    express = require('express'),
    app = express();
app.use(express.static('client'))
app.listen(80, () => console.log('Running server on port 80.'))
