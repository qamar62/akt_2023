const app = Vue.createApp({
         data() {
             return {
               BookingDate : "",
               Adult:  1,
               Children: 0,
               Infant: 0,
             
             }
           }, 
           methods: {
                incrementAdult(){
                  this.Adult++
                  localStorage.setItem("Adult", this.Adult)
                  localStorage.setItem("BookingDate", this.BookingDate)
                  
                },
                incrementChildren(){
                  this.Children++
                  localStorage.setItem("Children", this.Children)
                },
                decrementAdult(){
                  this.Adult--
                  localStorage.setItem("Adult", this.Adult)
                  if (this.Adult <= 0) {
                    this.Adult = 1
                  }
                },
                decrementChildren(){
                  this.Children--
                  localStorage.setItem("Children", this.Children)
                  if (this.Children <= 0) {
                    this.Children = 0
                  }
                },
                incrementInfant(){
                  this.Infant++
                  localStorage.setItem("Infant", this.Infant)
                },
              },
              decrementInfant(){
                this.Infant--
                localStorage.setItem("Infant", this.Infant)
                if (this.Infant <= 0) {
                  this.Infant = 0
                }
           },
     })
app.mount("#canvas")


const appBooking = Vue.createApp({
         data() {
             return {
               Adult:  localStorage.getItem("Adult"),
               Children: localStorage.getItem("Children"),
               Infant : localStorage.getItem("Infant"),
             
             }
           }, 
          
     })
     appBooking.mount("#personData")

