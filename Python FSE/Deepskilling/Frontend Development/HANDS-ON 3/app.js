import { courses } from "./data.js";

// ES6 Destructuring

courses.forEach(course=>{

    const {name,credits}=course;

    console.log(`${name} : ${credits} Credits`);

});

// map()

const formattedCourses=courses.map(course=>
`${course.code} - ${course.name} (${course.credits} credits)`
);

console.log(formattedCourses);

// filter()

const filteredCourses=courses.filter(course=>course.credits>=4);

console.log("Courses with Credits >=4 :",filteredCourses.length);

// reduce()

const totalCredits=courses.reduce(
(sum,course)=>sum+course.credits,0
);

console.log("Total Credits :",totalCredits);

// DOM

const grid=document.querySelector(".course-grid");

const total=document.getElementById("total-credits");

const selected=document.getElementById("selected-course");

function renderCourses(courseList){

    grid.innerHTML="";

    courseList.forEach(course=>{

        const article=document.createElement("article");

        article.className="course-card";

        article.dataset.id=course.id;

        article.innerHTML=`

        <h3>${course.name}</h3>

        <p>${course.code}</p>

        <p>Credits : ${course.credits}</p>

        `;

        grid.appendChild(article);

    });

    total.textContent=`Total Credits : ${courseList.reduce(
    (sum,c)=>sum+c.credits,0)}`;

}

renderCourses(courses);

// Search

const search=document.getElementById("search-courses");

search.addEventListener("input",()=>{

    const value=search.value.toLowerCase();

    const filtered=courses.filter(course=>

    course.name.toLowerCase().includes(value)

    );

    renderCourses(filtered);

});

// Sort

document.getElementById("sort-btn").addEventListener("click",()=>{

    const sorted=[...courses].sort(

    (a,b)=>b.credits-a.credits

    );

    renderCourses(sorted);

});

// Event Delegation

grid.addEventListener("click",(event)=>{

    const card=event.target.closest(".course-card");

    if(!card) return;

    const id=Number(card.dataset.id);

    const course=courses.find(c=>c.id===id);

    selected.textContent=

    `Selected Course : ${course.name}
     | Grade : ${course.grade}`;

});