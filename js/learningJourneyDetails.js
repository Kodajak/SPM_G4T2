const vm = new Vue({
    el: '#main-container',
    data: {
        staffId: 160212,
        selectedLj: '',
        ljDetails: '',
        addCourseButton: false,
        removeCourseButton: true,
        availCourses: '',
        noNewCourseList: []

    },

    methods: {
        viewAllLearningJourneys: function() {
            return window.location.replace("./myLearningJourney.html");
        },

        viewLearningJourney: function(selectedLj) {
        console.log(selectedLj)
        axios.post('http://localhost:5000/view_LjDetails/' + selectedLj, {
            selectedLj: selectedLj
        }) 
        .catch(error => alert(error))
        },

        deleteLearningJourney: function(selectedLj) {
            a = confirm("Are you sure you want to delete this learning journey?")
            if (a == true) {
                axios.delete('http://localhost:5000/deleteLearningJourney/' + selectedLj, {
                    selectedLj: selectedLj
                }) 
                .then(response=> {
                    alert("You have successfully delete a learning journey")
                    return window.location.replace("./myLearningJourney.html");
                })
                .catch(error => alert(error))
            }
        }
    },

    mounted: function() {
        let urlParams = new URLSearchParams(window.location.search);
        let myParam = urlParams.get('ljourney_id');
        axios.get('http://localhost:5000/view_LjDetails/' + myParam)
            .then(response => {
                this.ljDetails = response.data.data

                axios.get('http://localhost:5000/viewCoursesToAdd/' + myParam)
                .then(response => {
                    this.availCourses = response.data.data
                    for (skill of this.availCourses[2]) {
                        if (skill[1] != '') {
                            skillId = skill[0][0]
                            
                            if (skill[1].length == 0) {
                                console.log(skill[1])
                                this.noNewCourseList.push(skillId)
                            }

                            let completed_count = 0

                            // if there are courses that are not completed, show add courses button

                            for (course of skill[1]) {
                                if (course[2] != 'Completed') {
                                    // console.log(course[2])
                                    this.addCourseButton = true
                                } else if (course[2] == 'Completed'){
                                    completed_count += 1
                                }
                        
                            }
                            if (completed_count == skill[1].length) {
                                this.noNewCourseList.push(skillId)
                            }

                        }
                    }
                    
                })
                .catch(error => alert(error));


            })
            .catch(error => alert(error));
    }
})