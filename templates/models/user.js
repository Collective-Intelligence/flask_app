/**
 *  User Settings Schema
 *  @author Una Ada (Trewbot) <una@phene.co>
 * 
 *  This file isn't meant as operable code, but as a descriptor of what info-
 *  -rmation needs to be able to be derived from requests to the server from the
 *  client JavaScript. Preferably, this would be sent as a JSON string such that
 *  the client would be able to parse this into a JavaScript object and save it
 *  as a session state.
 *
 *  TODO: Update backend variables when documentation is available.
 */

//  Subtypes
const Column = {
    contains: [String],     //  List of moduleids contained in the column
    width: Number           //  Width of the column in pixels
};
const Token = {
    perm: String
    temp: String
};

//  User schema
const User = {
    account: String,
    adToken: Token,
    display: String,        //  Name to be displayed for the user
    experience: Number,
    gp: Number,
    owed: Number,
    reviewToken: String,
    type: "Account",
    ui: {
        accent: String      //  Accent color for display
        columns: [Column]   //  Columns to be rendered in the client
    },
    upvoteToken: Token,
    username: String        //  Internal name for user (possibly displayed)
};
