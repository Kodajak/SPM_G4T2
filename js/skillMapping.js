let urlParams = new URLSearchParams(window.location.search);
let myParam = urlParams.get('skill_id');
const vm = new Vue({
    el: '#main-container',
    data: {
        skills: [],
        courses: [],
        roles: []
    },
    methods:{
        removeCourse: function(value,value2) {
            if(this.courses.length === 1){
                alert("You must have more than 1 course to remove mapping ")
            } else {
                proceed = confirm("Are you sure you want to remove " + value2 + " ?")
                event.preventDefault();
                if (proceed === true) {
                    axios.post('http://localhost:5000/removeCourseMapping/'+myParam, {
                        course: value
                    })
                    .then(response => {
                            window.location.replace("./skillMapping.html?skill_id="+myParam);
                            return alert("You have successfully removed " + value2 + " !")
                        })
                    .catch(error => { 
                        this.error = error.response.data.message 
                        if (this.error != '') {
                            return alert(this.error)
                        }
                    });
                }
            }              
        },
        removeRole: function(value, value2){
            if(this.roles.length === 1){
                alert("You must have more than 1 role to remove mapping ")
            } else {
                proceed = confirm("Are you sure you want to remove " + value2 + " ?")
                event.preventDefault();
                if (proceed === true) {
                    console.log(value)
                    axios.post('http://localhost:5000/removeRoleMapping/'+myParam, {
                        role: value
                    })
                    .then(response => {
                            window.location.replace("./skillMapping.html?skill_id="+myParam);
                            return alert("You have successfully removed " + value2 + " !")
                        })
                    .catch(error => { 
                        this.error = error.response.data.message 
                        if (this.error != '') {
                            return alert(this.error)
                        }
                    });
                }
            }
            
        }

    },
    mounted: function() {
        
        axios.get('http://localhost:5000/view-skill-mapping/'+myParam )
            .then(response => {
                this.skills = response.data.skill,
                this.courses = response.data.courses,
                this.roles = response.data.roles
            })
            .catch(error => alert(error));
    }
});