homeTeamSelected = "Atlanta Hawks"
awayTeamSelected = "Boston Celtics"
function test() {
    console.log(homeTeamSelected)
    console.log(awayTeamSelected)
}
function addNumbers() {
    fetch('http://63.34.29.80:5000/api/get_prediction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ num1: homeTeamSelected, num2: awayTeamSelected })
    })
        .then(response => response.json())
        .then(data => {
            //document.getElementById('result').textContent = 'Result: ' + data.result;
            //document.getElementById('Vainqueur').innerHTML = ""
            document.getElementById('Vainqueur').innerHTML = "Vainqueur : <img src='img/" + data.result + ".png' class='logoTeam'>  " + data.result;
        })
        .catch(error => console.error('Error:', error));
}
function generateTableRows(data) {
    var dpHome = document.getElementById("dpHome");
    var dpAway = document.getElementById("dpAway");
    var rowHome = "";
    var rowAway = "";
    let nbaTeams = [
        "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
        "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
        "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
        "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
        "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
        "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns",
        "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors",
        "Utah Jazz", "Washington Wizards"
    ];

    for (let team of nbaTeams) {
        rowHome += "<a class='dropdown-item' href='#' onclick=\"changeHomeTeamSelected('" + team + "')\"" + ">" + team + "</a>"
        rowAway += "<a class='dropdown-item' href='#' onclick=\"changeAwayTeamSelected('" + team + "')\"" + ">" + team + "</a>"
    }
    dpHome.innerHTML += rowHome;
    dpAway.innerHTML += rowAway;
}
function changeHomeTeamSelected(newHomeTeamSelected) {
    homeTeamSelected = newHomeTeamSelected
    //console.log(homeTeamSelected)
    homeTeamLogo = document.getElementById("homeTeamLogo")
    homeTeamLogo.innerHTML = ''
    homeTeamLogo.innerHTML = "<img src='img/" + homeTeamSelected + ".png ' class='logoTeamPred'>"
}
function changeAwayTeamSelected(newAwayTeamSelected) {
    awayTeamSelected = newAwayTeamSelected
    //console.log(awayTeamSelected)
    awayTeamLogo = document.getElementById("awayTeamLogo")
    awayTeamLogo.innerHTML = ''
    awayTeamLogo.innerHTML = "<img src='img/" + awayTeamSelected + ".png ' class='logoTeamPred'>"
}
function main() {
    generateTableRows()
}