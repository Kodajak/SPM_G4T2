const vm = new Vue({
    el: '#main-container',
    data: {
        courses: [],
        statusOfImport: ''
    },
    mounted: function() {
        
        axios.get('http://localhost:5000/statusOfImportSuc')
            .then(response => {
                this.msg = response.data.msg
                window.location.replace("./coursesManagement.html");
                return alert(this.msg);
                 
            })
            .catch(error => alert(error));
    }
});