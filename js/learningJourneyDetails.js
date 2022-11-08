const vm = new Vue({
    el: '#main-container',
    data: {
        staffId: 160212,
        selectedLj: '',
        ljDetails: '',
        addCourseButton: false,
        removeCourseButton: false,
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
                                if (this.addCourseButton == true) {
                                    break
                                }
                                if (course[2] != 'Completed') {
                                    this.addCourseButton = true
                                    var btn = document.createElement("button");  
                                    btn.innerHTML = "Add Courses"
                                    
                                    let addCourseLink = './addLearningJourneyCourse.html?ljourney_id=' + this.ljDetails[0]
                                    
                                    btn.onclick = function() {
                                        return window.location.replace(addCourseLink)
                                    }

                                    btn.className = 'btn btn-outline-secondary'

                                    document.getElementById("updateButtons").appendChild(btn)
                                    
                                    break
                                } 
                                else if (course[2] == 'Completed'){
                                    completed_count += 1
                                }
                            }
                            if (completed_count == skill[1].length) {
                                this.noNewCourseList.push(skillId)
                            }

                        }
                    }

                    // if there is only 1 Unique course selected, hide remove button
                    let tempCourseList = []
                        for (skill of this.ljDetails[2]) {
                            skillCourseList = skill[1]
                            
                            if (skillCourseList.length != 0) {
                                courseId = skillCourseList[0][0]
                                
                                // check if unique
                                if (!tempCourseList.includes(courseId)) {
                                    tempCourseList.push(courseId)
                                }
                            }
                        }
                        if (tempCourseList.length > 1) {  
                            var btn = document.createElement("button");  
                            btn.innerHTML = "Remove Courses"
                            
                            let removeCourseLink = './removeLearningJourneyCourse.html?ljourney_id=' + this.ljDetails[0]
                            
                            btn.onclick = function() {
                                return window.location.replace(removeCourseLink)
                            }

                            btn.className = 'btn btn-outline-danger ml-3'

                            document.getElementById("updateButtons").appendChild(btn)
                        }
                        console.log(tempCourseList)

                        
                        this.selectedLj = myParam
                    
                })
                .catch(error => alert(error));


            })
            .catch(error => alert(error));
    }
})
