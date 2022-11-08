function cancelLearningJourney() {
    window.location.replace("./myLearningJourney.html");
}

const vm = new Vue({
    el: '#main-container',
    data: {
        staffId: 160212,
        roles: [],
        selectedRole: '',
        skills: [],
        selectedSkill: '',
        courses: [],
        selectedCourses: [],
        error: ''
    },
    watch: {
        selectedRole: function (selectedRole) {
            axios.get('http://localhost:5000/view_skills/' + selectedRole[0])
            .then(response => {
                this.skills = response.data.data
            })
            .catch(error => alert(error));
        },

        selectedSkill: function (selectedSkill) {
            if (this.selectedSkill != '') {
                axios.get('http://localhost:5000/view-course-skills/'+ selectedSkill)
                .then(response => {
                    this.courses = response.data.data
                    console.log(this.courses)
                })
                .catch(error => alert(error));
            }
        }
    },
    methods: {
        onChange:function(){
            this.selectedSkill = ''
            this.selectedCourses = []
        },
        
        // submit LJ
        submitLearningJourney: function() {
            event.preventDefault(); 
            if (this.selectedRole == '') {
                return alert("Please select a role first.")
            } else if (this.selectedCourses.length == 0) {
                return alert("Please select at least 1 course.")
            }
            else {
                
                axios.post('http://localhost:5000/create_lj', {
                        staffId: this.staffId,
                        selectedRole: this.selectedRole,
                        selectedCourses: this.selectedCourses,
                    })
                .then(response => {
                        window.location.replace("./myLearningJourney.html");
                        
                        return alert("You have successfully created a learning journey.")
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
    // get roles from db
    mounted: function() {
        axios.get('http://localhost:5000/view_filteredLjRoles/' + this.staffId)
            .then(response => {
                // all roles
                this.roles = response.data.data
            })
            .catch(error => alert(error));
    }, 
})