function CourseCard({

    id,
    name,
    code,
    credits,
    grade,
    onEnroll

}){

    return(

        <div className="card">

            <h2>{name}</h2>

            <p>{code}</p>

            <p>Credits : {credits}</p>

            <p>Grade : {grade}</p>

            <button onClick={()=>onEnroll(id)}>

                Enroll

            </button>

        </div>

    );

}

export default CourseCard;