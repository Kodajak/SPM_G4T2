const vm = new Vue({
    el: '#main-container',
    data: {
        staffId: 160212,
        selectedLj: '',
        ljDetails: '',
        courses: [],
        selectedCourses: [],
    },

    methods: {
        cancelEdit: function() {
            return window.location.replace("./learningJourneyDetails.html/" + ljDetails[0]);
        },
        // submit LJ
        addCoursesToLj: function() {
            event.preventDefault(); 
            if (this.selectedCourses.length == 0) {
                return alert("Please select at least 1 course.")
            }
            else {
                
                axios.post('http://localhost:5000/addCoursesToLj', {
                        selectedLj: this.selectedLj,
                        selectedCourses: this.selectedCourses,
                    })
                .then(response => {
                        alert("You have successfully added " + this.selectedCourses.length.toString() + " new course(s) to your " + this.ljDetails[1] +" learning journey.")
                        
                        return window.location.replace("./learningJourneyDetails.html?ljourney_id=" + this.selectedLj);
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

    mounted: function() {
        let urlParams = new URLSearchParams(window.location.search);
        let myParam = urlParams.get('ljourney_id');
        axios.get('http://localhost:5000/viewCoursesToAdd/' + myParam)
            .then(response => {
                this.ljDetails = response.data.data
                this.selectedLj = myParam
            })
            .catch(error => alert(error));
    }
})
