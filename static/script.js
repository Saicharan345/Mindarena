let currentUser = null;

async function register(){
    let res = await fetch("/register",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            username: username.value,
            password: password.value
        })
    });

    let data = await res.json();

    if(data.status === "registered"){
        document.getElementById("loginMsg").innerText = "Registered successfully!";
    } else {
        document.getElementById("loginMsg").innerText = "User already exists!";
    }
}

async function login(){
    let res = await fetch("/login",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            username: username.value,
            password: password.value
        })
    });

    let data = await res.json();

    if(data.status === "success"){
        currentUser = username.value;
        document.getElementById("loginMsg").innerText = "Login successful!";
    } else {
        document.getElementById("loginMsg").innerText = "Invalid credentials!";
    }
}

async function checkWord(){

    if(!currentUser){
        alert("Please login first!");
        return;
    }

    let word = document.getElementById("wordInput").value;

    let res = await fetch("/validate",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({word})
    });

    let data = await res.json();

    if(data.valid){
        document.getElementById("message").innerText = "Correct! +" + word.length + " points";

        await fetch("/update_score",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({
                username: currentUser,
                points: word.length
            })
        });

    } else {
        document.getElementById("message").innerText = "Invalid!";
    }

    document.getElementById("wordInput").value = "";
}

async function loadLeaderboard(){
    let res = await fetch("/leaderboard");
    let data = await res.json();

    let board = document.getElementById("board");
    board.innerHTML = "";

    data.forEach(u=>{
        board.innerHTML += `<li>${u.username} - ${u.score}</li>`;
    });
}
