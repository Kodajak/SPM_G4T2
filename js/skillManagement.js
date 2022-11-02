const vm = new Vue({
    el: '#main-container',
    data: {
        allSkills: [],
        skillsWithCourses: [],
        skillsWithRoles:[],
        new_SkillName: '',
        new_SkillDesc: '',
        modalSkill: '',
        skillNametoEdit: this.modalSkill,
        skillDesctoEdit: this.modalSkill
    },
    methods:{
        sendInfo(skill) {
            this.modalSkill = skill;
            this.skillNametoEdit = skill[1]
            this.skillDesctoEdit = skill[2]
        },
        delete_Skill(skillToDelete){
            console.log(skillToDelete)
            axios.delete("http://localhost:5000/delete_Skill/" + skillToDelete[0])
                    .then(response=>{
                        window.location.reload()
                        console.log(response)
                    })
                    .catch(error=>{this.error = error.response })
        },
        switchStatus(skillToSwitch){
            console.log(skillToSwitch)
            if (skillToSwitch[3] == 1){
                axios.post("http://localhost:5000/switchStatus/" + skillToSwitch[0], {"data":[0]})
                    .then(response=>{
                        window.location.reload()
                        console.log(response)
                        return alert("Skill Deactivated!")
                    })
                    .catch(error=>{this.error = error.response})
            }
            else{
                axios.post("http://localhost:5000/switchStatus/" + skillToSwitch[0], {"data":[1]})
                    .then(response=>{
                        window.location.reload()
                        console.log(response)
                        return alert("Skill Activated!")
                    })
                    .catch(error=>{this.error = error.response})
            }
        },
        edit_Skill(){
            event.preventDefault()
            skillArr = []
            for (skill of this.allSkills){
                skillArr.push([skill[0], skill[1].toLowerCase(), skill[2].toLowerCase()])
            }

            this.skillNametoEdit = this.skillNametoEdit.trim()
            this.modalSkill[1] = this.skillNametoEdit
            this.skillDesctoEdit = this.skillDesctoEdit.trim()
            this.modalSkill[2] = this.skillDesctoEdit

            // console.log(skillArr)
            // console.log(this.modalSkill)
            // console.log([this.modalSkill[1].toLowerCase(), this.modalSkill[2].toLowerCase()])
            
            var error = false
            skillArr.forEach((row, index) => {
                // console.log(row[0], this.modalSkill[0])
                if (row[1] == this.modalSkill[1].toLowerCase() && row[2] == this.modalSkill[2].toLowerCase()) {
                    // console.log('true', row)
                    window.location.reload()
                    return alert("No changes made!")
                }
                else if (row[0] != this.modalSkill[0] && row[1] == this.modalSkill[1].toLowerCase()) {
                    window.location.reload()
                    error = true
                    return alert("Skill Name exists!")
                }
                else if (row[0] != this.modalSkill[0] && row[2] == this.modalSkill[2].toLowerCase()) {
                    window.location.reload()
                    error = true
                    return alert("Skill description exists!")
                }
            })
            if (this.modalSkill[1] != "" && this.modalSkill[2] != "" && error == false){
                        axios.post("http://localhost:5000/edit_Skill", {"data":[this.modalSkill]})
                            .then(response=>{
                                window.location.reload()
                                // console.log(response)
                                return alert("Skill updated!")
                            })
                            .catch(error=>{this.error = error.response})
                }
            else if (error == true) {
                return ""
            }
            else {
                window.location.reload()    
                return alert("Input field is empty!")
            }
        },                
        create_Skill(){
            event.preventDefault()
            console.log(this.new_SkillName)
            this.new_SkillName = this.new_SkillName.trim()
            this.new_SkillDesc = this.new_SkillDesc.trim()
            skillArr = []
                for (skill of this.allSkills){
                    skillArr.push(skill[1].toLowerCase())
                }
            skillDescArr = []
                for (skill of this.allSkills){
                    skillArr.push(skill[2].toLowerCase())
                }
            console.log(skillArr)
            if (skillArr.includes(this.new_SkillName.toLowerCase())) {
                this.new_SkillName = ""
                this.new_SkillDesc = ""
                return alert("Skill exists")
            }
            else if(skillArr.includes(this.new_SkillDesc.toLowerCase())){
                this.new_SkillName = ""
                this.new_SkillDesc = ""
                return alert("Skill description exists")
            }else if(this.new_SkillName=="" || this.new_SkillDesc==""){
                return alert("Skill Name/Description is blank!")
            }
            else{
                axios.post("http://localhost:5000/create_Skill", {"data":[this.new_SkillName, this.new_SkillDesc]})
                    .then(response=>{
                        window.location.reload()
                        console.log(response)
                        return alert("Skill created!")
                    })
                    .catch(error=>{this.error = error.response.data.message })
            }
        }
    },
    mounted: function() {
        axios.get('http://localhost:5000/view_Skills')
            .then(response => {
                this.allSkills = response.data.data
                console.log(response.data.data) 
                axios.get('http://localhost:5000/get_CourseSkill')
                    .then(response2 => {
                        var skillCourseArr = []
                        for (const courseSkillPair of response2.data.data){
                            if (skillCourseArr.includes(courseSkillPair[1]) == false){
                                skillCourseArr.push(courseSkillPair[1])
                            }
                        }
                        this.skillsWithCourses = skillCourseArr

                        axios.get('http://localhost:5000/get_RoleSkill')
                            .then(response3 => {
                                var skillRoleArr = []
                                for (const courseSkillPair of response3.data.data){
                                    if (skillRoleArr.includes(courseSkillPair[1]) == false){
                                        skillRoleArr.push(courseSkillPair[1])
                                    }
                                }
                                this.skillsWithRoles = skillRoleArr
                            })
                    })
            })
            .catch(error => alert(error));
    }
});