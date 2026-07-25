import {useState} from "react";

function StudentProfile(){

const [name,setName]=useState("");

const [email,setEmail]=useState("");

const [semester,setSemester]=useState("");

return(

<div className="profile">

<h2>Student Profile</h2>

<input
placeholder="Name"
value={name}
onChange={(e)=>setName(e.target.value)}
/>

<input
placeholder="Email"
value={email}
onChange={(e)=>setEmail(e.target.value)}
/>

<input
placeholder="Semester"
value={semester}
onChange={(e)=>setSemester(e.target.value)}
/>

<h3>{name}</h3>
<p>{email}</p>
<p>{semester}</p>

</div>

);

}

export default StudentProfile;