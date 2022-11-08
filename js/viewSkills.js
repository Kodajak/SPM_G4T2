const vm = new Vue({
    el: '#main-container',
    data: {
        skills : []
    },
    mounted: function() {
        axios.get('http://localhost:5000/view_Skills' )
            .then(response => {
                this.skills = response.data.data
            })
            .catch(error => alert(error));
    }
});