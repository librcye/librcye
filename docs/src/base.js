var DATA = "../../data"
var CENSORED_PATH = DATA+"censored"
var UNCENSORED = DATA+"uncensored"
var NEWLY = DATA+"newly_censored"
var RAW_HOST = "https://raw.githubusercontent.com/librcye/data/master/"
var countries_records = [] // as read from raw countries file
var countries = [] //unique countries. in form NAME_CODE
var SEP = ","

function getCensoredCountries() {
    var request = new XMLHttpRequest()
    request.onreadystatechange = function() {
	if (this.status==200)
	    countries_records = this.responseText.split('\n')
    }
    request.open('GET', RAW_HOST+"countries")
    request.send()
    for (var i = 0; i < countries_records.length; i++)
	countries.push(countries_records[i].split('_', 1).toLowerCase())
    return countries
}

function load_records() {
    records = []
    var request
    for (var i = 0; i < countries_records.length; i++) {
	metadata = countries_records[i].split('_')
	request = new XMLHttpRequest()
	request.onreadystatechange = function() {
	    if (this.status==200) //TODO check 2xx
		//TODO complete adapter
		records.push([metadata, this.responseText.split('\n')])
	}
	request.open('GET', RAW_HOST+countries_records[i]+'.txt')
	request.sent()
    }
    return records
}
