
const app = Vue.createApp({
         data() {
             return {
               Adult:  1,
               Children: 0,
               Infant: 0,
             
             }
           }, 
           methods: {
                if(localStorage){
                    localStorage.setItem("Adult", this.Adult)
                }
           },
     })
app.mount("#canvas")