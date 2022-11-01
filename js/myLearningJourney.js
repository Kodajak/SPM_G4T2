function createLearningJourney() {
    window.location.replace("./createLearningJourney.html");
}

const vm = new Vue({
    el: '#main-container',
    data: {
        staffId: 160212,
        lj: []
    },

    methods: {
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
                return window.location.reload()
            })
            .catch(error => alert(error))
        }
    }
},

    mounted: function() {
        axios.get('http://localhost:5000/view_AllLj/' + this.staffId)
            .then(response => {
                this.lj = response.data.data
            })
            .catch(error => alert(error));
    }
})