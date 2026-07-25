import {useState,useEffect} from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import CourseCard from "./components/CourseCard";
import StudentProfile from "./components/StudentProfile";
import "./App.css";

function App(){

const [courses,setCourses]=useState([]);
const [loading,setLoading]=useState(true);
const [error,setError]=useState("");
const [searchTerm,setSearchTerm]=useState("");
const [enrolledCourses,setEnrolledCourses]=useState([]);

useEffect(()=>{

async function loadCourses(){

try{

const response=await fetch("https://jsonplaceholder.typicode.com/posts?_limit=5");

const data=await response.json();

const mapped=data.map((post,index)=>({

id:post.id,
name:post.title,
code:`CS10${index+1}`,
credits:4,
grade:"A"

}));

setCourses(mapped);

}catch{

setError("Unable to load courses");

}finally{

setLoading(false);

}

}

loadCourses();

},[]);

useEffect(()=>{

console.log("Courses updated");

// Runs only when courses change because
// courses is in the dependency array.

},[courses]);

const handleEnroll=(id)=>{

const selected=courses.find(course=>course.id===id);

if(selected){

setEnrolledCourses([...enrolledCourses,selected]);

}

};

const filteredCourses=courses.filter(course=>

course.name.toLowerCase().includes(searchTerm.toLowerCase())

);

return(

<>

<Header
siteName="Student Portal"
enrolledCount={enrolledCourses.length}
/>

<div className="container">

<input
type="text"
placeholder="Search courses..."
value={searchTerm}
onChange={(e)=>setSearchTerm(e.target.value)}
/>

{loading && <h2>Loading...</h2>}

{error && <h2>{error}</h2>}

<div className="grid">

{!loading &&
filteredCourses.map(course=>(

<CourseCard
key={course.id}
{...course}
onEnroll={handleEnroll}
/>

))}

</div>

<StudentProfile/>

</div>

<Footer/>

</>

);

}

export default App;