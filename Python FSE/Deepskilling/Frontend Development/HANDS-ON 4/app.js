import { courses } from "./data.js";

const grid = document.querySelector(".course-grid");
const loading = document.getElementById("loading");
const spinner = document.getElementById("spinner");
const notificationSection =
document.getElementById("notifications");

const retryBtn =
document.getElementById("retryBtn");

const error =
document.getElementById("error");


// ----------------------------
// Task 45
// Promise with then()
// ----------------------------

function fetchUser(id){

return fetch(
`https://jsonplaceholder.typicode.com/users/${id}`
)
.then(response=>response.json())
.then(user=>{

console.log("User :",user.name);

});

}

fetchUser(1);


// ----------------------------
// Task 46
// async await
// ----------------------------

async function fetchUserAsync(id){

try{

const response=await fetch(

`https://jsonplaceholder.typicode.com/users/${id}`

);

const user=await response.json();

console.log("Async User :",user.name);

}

catch(err){

console.log(err);

}

}

fetchUserAsync(2);


// ----------------------------
// Task 47 & 48
// Loading Courses
// ----------------------------

function fetchAllCourses(){

return new Promise(resolve=>{

setTimeout(()=>{

resolve(courses);

},1000);

});

}

function renderCourses(courseList){

grid.innerHTML="";

courseList.forEach(course=>{

const article=document.createElement("article");

article.className="course-card";

article.innerHTML=`

<h3>${course.name}</h3>

<p>${course.code}</p>

<p>Credits : ${course.credits}</p>

`;

grid.appendChild(article);

});

}

loading.style.display="block";

fetchAllCourses().then(result=>{

loading.style.display="none";

renderCourses(result);

});


// ----------------------------
// Task 49
// Promise.all()
// ----------------------------

Promise.all([

fetch("https://jsonplaceholder.typicode.com/users/1")
.then(res=>res.json()),

fetch("https://jsonplaceholder.typicode.com/users/2")
.then(res=>res.json())

]).then(users=>{

console.log(users[0].name);

console.log(users[1].name);

});


// ----------------------------
// Task 50
// apiFetch()
// ----------------------------

async function apiFetch(url){

const response=await fetch(url);

if(!response.ok){

throw new Error("Unable to fetch data.");

}

return response.json();

}


// ----------------------------
// Task 51-54
// Notifications
// ----------------------------

async function loadNotifications(){

spinner.style.display="block";

notificationSection.innerHTML="";

error.textContent="";

retryBtn.style.display="none";

try{

const posts=await apiFetch(

"https://jsonplaceholder.typicode.com/posts?_limit=5"

);

spinner.style.display="none";

posts.forEach(post=>{

const div=document.createElement("div");

div.className="notification";

div.innerHTML=`

<h3>${post.title}</h3>

<p>${post.body}</p>

`;

notificationSection.appendChild(div);

});

}

catch(err){

spinner.style.display="none";

error.textContent=

"Something went wrong. Please try again.";

retryBtn.style.display="inline";

}

}

loadNotifications();


// Simulate 404

apiFetch(

"https://jsonplaceholder.typicode.com/nonexistent"

).catch(()=>{

error.textContent="404 Error Occurred.";

retryBtn.style.display="inline";

});


retryBtn.addEventListener(

"click",

loadNotifications

);


// ----------------------------
// Task 55-59
// Axios
// ----------------------------


// Interceptor

axios.interceptors.request.use(config=>{

console.log(

"API call started :",config.url

);

return config;

});


// Axios Version

async function apiFetchAxios(url){

const response=await axios.get(url);

return response.data;

}


// Fetch posts of user 1

axios.get(

"https://jsonplaceholder.typicode.com/posts",

{

params:{

userId:1

}

}

).then(response=>{

console.log(

"Axios Posts",

response.data

);

});


/*

FETCH

1. Built into browser

2. Must use response.json()

3. Need response.ok checking


AXIOS

1. External library

2. JSON parsed automatically

3. Automatically throws error for HTTP errors

*/