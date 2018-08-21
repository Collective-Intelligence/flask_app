async function retrAcc(username, log=false) {
	var account;
	await steem.api.getAccounts([username], (err, result) => {
		if (err == null) {
			account = result[0];
		} else {
			console.log(err);
			account = false;
		}
	});

	return new Promise ((resolve, reject) => {
		setTimeout(function() {
			if (log) { console.log(account); }
			resolve(account);
		}, 2000);
	});
}

async function retrMemos(username, log=false) {
	var old_history, history = [];
	await steem.api.getAccountHistory(username, "-1", "100", (err, result) => {
		if (err == null) {
			old_history = result;
		} else {
			console.log(err);
			old_history = false;
		}

		if (old_history != false) {
			for (var i = 0; i < old_history.length; i++) {
				if (old_history[i][1]["op"][0] == "transfer") {
					try {
						if (old_history[i][1]["op"][1]["memo"] != false) {
							history.push(old_history[i][1]["op"][1]["memo"]);
						}
					} catch(e) {
						console.log(e);
					}
				}
			}
		} else {
			history = false;
		}
	});

	return new Promise ((resolve, reject) => {
		setTimeout(() => {
			if (log) { console.log(history); }
			resolve(history);
		}, 2000);
	});
}

function filterTrending(data) {
	trending = [];
    for (var i = data.length - 1; i >= 0; i--) {
    	parsed = JSON.parse(data[i]);
        if (parsed['type'] == "trending" && parsed['posts'].length > 0) {
        	trending.push(parsed);
        }
    }
    return trending;
}

async function getPost(username, permalink) {
	var result = [];
	await steem.api.getContent(username, permalink, function(err, qresult) {
		result = qresult;
	});

	return new Promise((resolve, reject) => {
		setTimeout(() => {
			resolve(result);
		}, 2000);
	});
}

function getTrending(username="comedy-central", limLow=0, limHigh=1) {
	retrMemos(username).then(data => {
	    trending = filterTrending(data); //I wanna have it add all the posts into a single list at some point
	    for (i = limLow; i < limHigh; i++) {
	    	for (j = 0; j < trending[i]['posts'].length; j++) {
	    		var post = trending[i]['posts'][j][1].split("/");
	    		getPost(post[0], post[1]).then(data2 => {
	    			console.log(data2);
	    			tags = "";
	    			tagsLinks = "";
	    			for (n = 0; n < JSON.parse(data2['json_metadata'])['tags'].length; n++) {
	    				tag = JSON.parse(data2['json_metadata'])['tags'][n];
	    				tags = tags.concat(tag, " ");
	    				tagsLinks = tagsLinks.concat("<a target=\"_BLANK\" href=\"https://steemit.com/trending/", tag, "\">", tag, "</a> ")
	    			}
	    			if (data2['body'].match(/<\/?.*\/?>/) !== null) {
	    				$("div#content").append(
		    				"<div class=\"".concat(
		    					"featured-post ", data2['author'], " ", tags,
		    					"\"><h2>",
		    					data2['title'], 
		    					"<span class=\"link\"><a target=\"_BLANK\" href=\"https://steemit.com",
		    					data2['url'],
		    					"\">🔗</a></span></h2><p class=\"tags\">by <a target=\"_BLANK\" href=\"https://steemit.com/@",
		    					data2['author'],
		    					"\">",
		    					data2['author'],
		    					"</a> in ",
		    					tagsLinks,
		    					"</p></p><p>", 
		    					data2['body']
		    						//.replace(/(?:\r\n|\r|\n)/g, "<br />")
		    						.replace(/https:\/\/imgur/g, "https://i.imgur")
		    						.replace(/http([A-z0-9\-\_\.\/\:]+)\.(png|jpe?g|gif)/g, x => {return "<img style=\"width:100%\" src=\"".concat(x, "\" />")})),
		    						//.replace(/http([A-z0-9\-\_\.\/\:]+)\.(png|jpe?g|gif)/g, x => {return "![Image loading...](".concat(x, ")")})),
		    					"</p></div><hr />"
		    				);
	    			} else {
		    			$("div#content").append(
		    				"<div class=\"".concat(
		    					"featured-post ", data2['author'], " ", tags,
		    					"\"><h2>",
		    					data2['title'], 
		    					"<span class=\"link\"><a target=\"_BLANK\" href=\"https://steemit.com",
		    					data2['url'],
		    					"\">🔗</a></span></h2><p class=\"tags\">by <a target=\"_BLANK\" href=\"https://steemit.com/@",
		    					data2['author'],
		    					"\">",
		    					data2['author'],
		    					"</a> in ",
		    					tagsLinks,
		    					"</p></p><p>", 
		    					Markdown.toHTML(data2['body']
		    						//.replace(/(?:\r\n|\r|\n)/g, "<br />")
		    						.replace(/https:\/\/imgur/g, "https://i.imgur")
		    						//.replace(/http([A-z0-9\-\_\.\/\:]+)\.(png|jpe?g|gif)/g, x => {return "<img style=\"width:100%\" src=\"".concat(x, "\" />")})),
		    						.replace(/http([A-z0-9\-\_\.\/\:]+)\.(png|jpe?g|gif)/g, x => {return "![Image loading...](".concat(x, ")")})),
		    					"</p></div><hr />")
		    				);
		    		}
	    		});
	    	}
	    }
	});
}