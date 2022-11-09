let urlParams = new URLSearchParams(window.location.search);
let myParam = urlParams.get('skill_id');
const vm = new Vue({
    el: '#main-container',
    data: {
        roles: [],
        selectedRoles: [],
        skills: [],
        courses: [],
        selectedCourses: [],
        error: '',
        currentMappedCourses: [],
        currentMappedRoles: []
    },
    methods: {
        // submit mappings
        submitMapping: function() {
                proceed = confirm("Are you sure you want to proceed with mapping ?")
                event.preventDefault();
                if(proceed == true){
                    if(this.selectedCourses.length + this.selectedRoles.length == 0){
                        return alert("Please select at least 1 Course/Role !")
                    }
                    console.log('SELECTED ' + this.selectedRoles + ' AND ' + this.selectedCourses)
                    console.log('CURRENT ' + this.currentMappedCourses + ' AND ' + this.currentMappedRoles)
                    axios.post('http://localhost:5000/submit-mapping/'+myParam, {
                            selectedRoles: this.selectedRoles,
                            selectedCourses: this.selectedCourses,
                            currentMappedCourses: this.currentMappedCourses,
                            currentMappedRoles: this.currentMappedRoles
                        })
                    .then(response => {
                            window.location.replace("./skillMapping.html?skill_id="+myParam);
                            return alert("You have successfully done your mapping.")
                        })
                    .catch(error => { 
                        this.error = error.response.data.message 
                        window.location.replace("./skillMapping.html?skill_id="+myParam);
                        return alert(this.error)
                    });
                }
            
        }
    },
    // get etc from db
    mounted: function() {
        axios.get('http://localhost:5000/update-skill-mapping/'+myParam)
            .then(response => {
                this.courses = response.data.courses,
                this.roles = response.data.roles,
                this.skills = response.data.skill,
                this.currentMappedCourses = response.data.currentMappedCourses,
                this.currentMappedRoles = response.data.currentMappedRoles
            })
            .catch(error => alert(error));
    }, 
})