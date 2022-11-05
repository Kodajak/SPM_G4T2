const vm = new Vue({
    el: '#main-container',
    data: {
        staffId: 160212,
        selectedLj: '',
        ljDetails: '',
        courses: [],
        selectedCourses: [],
        currentTotalCourses: 0,
    },

    methods: {
        cancelEdit: function() {
            return window.location.replace("./learningJourneyDetails.html/" + ljDetails[0]);
        },
        // remove courses from learning journey
        removeCourseFromLj: function() {
            console.log(this.selectedCourses)
            event.preventDefault(); 
            if (this.selectedCourses.length == 0) {
                return alert("Please select at least 1 course.")
            }

            else if (this.selectedCourses.length == this.currentTotalCourses) {
                return alert("You must have at least 1 course in the learning journey after deletion.")
            }
            
            else {

                a = confirm("Are you sure you want to delete the selected courses from your learning journey?")
                if (a == true) {
                
                    axios.post('http://localhost:5000/removeCoursesFromLj', {
                            selectedLj: this.selectedLj,
                            selectedCourses: this.selectedCourses,
                        })
                    .then(response => {
                            alert("You have successfully removed " + this.selectedCourses.length.toString() + " course(s) from your " + this.ljDetails[1] +" learning journey.")
                            
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
        }
    },

    mounted: function() {
        let urlParams = new URLSearchParams(window.location.search);
        let myParam = urlParams.get('ljourney_id');
        axios.get('http://localhost:5000/view_LjDetails/' + myParam)
            .then(response => {
                this.ljDetails = response.data.data
                let tempCourseList = []
                for (skill of this.ljDetails[2]) {
                    skillCourseList = skill[1]
                    
                    if (skillCourseList.length != 0) {
                        if (skillCourseList.length == 1) {
                            courseId = skillCourseList[0][0]
                            if (!tempCourseList.includes(courseId)) {
                                tempCourseList.push(courseId)
                            }
                        }
                        else {
                            for (course of skillCourseList) {
                                courseId = course[0]
                                if (!tempCourseList.includes(courseId)) {
                                    tempCourseList.push(courseId)
                                }
                            }
                        }
                    }
                }

                this.currentTotalCourses = tempCourseList.length
                console.log(this.currentTotalCourses)
    
                this.selectedLj = myParam
            })
            .catch(error => alert(error));
    }
})