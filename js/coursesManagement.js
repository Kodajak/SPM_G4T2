const vm = new Vue({
    el: '#main-container',
    data: {
        courses: [],
        statusOfImport: ''
    },
    methods: {
        validateImport: function(){
            if($("#file").val() === ''){
                alert("Please select a CSV File to import!");
            } else {
                const media_file = document.getElementById("file").value // event is from the <input> event
                const filename = media_file.split(/[,/\\]/)
                const file = filename.slice(-1)[0]
                importYes = confirm('Are you sure you want to import '+file +' ?');
                if (importYes === true){
                    document.getElementById("importlms").submit();
                }
            }
        }
    },
    mounted: function() {
        // let urlParams = new URLSearchParams(window.location.search);
        // let myParam = urlParams.get('err');
        // console.log(myParam)
        // this.alertMsg()
        axios.get('http://localhost:5000/view-course-list')
            .then(response => {
                this.courses = response.data.courses
            })
            .catch(error => alert(error));
    }
});