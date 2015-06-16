$.fn.ploneCatalogQueryToJSON = function() {

    console.log($(this).serializeJSON());

    // Define internal methods to generate canned data structures
    // =========================================================================
    
    // Used as a query string for the SearchableText
    function _query_string(v) {
        return {
            "query": { 
                "query_string": {
                    "query": v
                }
            }
        }
    }

    // For indexes with multiple parameters
    function _or(k, v) {
        var q = {
            or: {
                filters: []
            }
        }
        
        for (var i in v) {
            q["or"]["filters"].push(_match(k,v[i]));
        }
        
        return q;
    }
    
    // For indexes with one parameter
    function _match(k,v) {
        var q = {
			"query": {
				"match": {}
			}
        }

        q["query"]["match"][k] = { "query": v };

        return q;
    }


    // Define base JSON structure
    var q = {
    	"query": {
    		"filtered": {
            	}
    	}
	}
	
	// m is for "must"
    var m = [];
    
    // Loop through object for keys, and add filters onto "must" m array
    var form_json = $(this).serializeJSON()
    for (var k in form_json) {
        v = form_json[k];

        if (k == "SearchableText") {
            m.push(_query_string(v));
        }
        else if ($.isArray(v)) {
            m.push(_or(k,v));
        }
        else {
            m.push(_match(k,v));
        }
    }
    
    // Add filters to query
    q["query"]["filtered"] = {
        filter: {
            bool: {
                must: m
            }
        }
    }

    // Log query
    console.log(JSON.stringify(q));
    
    // and pass it back
    return q

}