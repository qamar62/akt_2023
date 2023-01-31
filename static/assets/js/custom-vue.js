const app = Vue.createApp({
         data() {
             return {
               BookingDate : "",
               Adult:  0,
               Children: 0,
               Infant: 0,
               adult_price : 350 ,
               child_price : 250 ,
               infant_price : 150 ,
               adultTotal : 0,
               childTotal:0,
               infantTotal:0,
               subTotal: "",
               
             
             }
           }, 
           methods: {
                 
                incrementAdult(){
                  this.Adult++
                  localStorage.setItem("Adult", this.Adult)
                  
                  this.adultTotal = (this.Adult * this.adult_price)
                  this.subTotal = (this.adultTotal + this.childTotal)
                  localStorage.setItem("subTotal", this.subTotal)
                  localStorage.setItem("adultTotal", this.adultTotal)
                  
                  
                },
                incrementChildren(){
                  this.Children++
                  localStorage.setItem("Children", this.Children)
                  this.childTotal = (this.Children * this.child_price)
                  this.subTotal = (this.adultTotal + this.childTotal)
                  localStorage.setItem("subTotal", this.subTotal)
                  localStorage.setItem("childTotal", this.childTotal)
                  
                },
                decrementAdult(){
                  this.Adult--
                  localStorage.setItem("Adult", this.Adult)
                  if (this.Adult <= 0) {
                    this.Adult = 1
                  }
                  this.adultTotal = (this.Adult * this.adult_price)
                  this.subTotal = (this.adultTotal + this.childTotal)
                  localStorage.setItem("subTotal", this.subTotal)
                  
                  
                },
                decrementChildren(){
                  this.Children--
                  localStorage.setItem("Children", this.Children)
                  if (this.Children <= 0) {
                    this.Children = 0
                  }
                  this.childTotal = (this.Children * this.child_price)
                  this.subTotal = (this.adultTotal + this.childTotal)
                  localStorage.setItem("subTotal", this.subTotal)
                  
                },
                incrementInfant(){
                  this.Infant++
                  localStorage.setItem("Infant", this.Infant)
                  this.infantTotal = (this.Infant * this.infant_price)
                  this.subTotal = (this.adultTotal + this.childTotal + this.infantTotal)
                  localStorage.setItem("subTotal", this.subTotal)
                },
                decrementInfant(){
                  this.Infant--
                  localStorage.setItem("Infant", this.Infant)
                  if (this.Infant <= 0) {
                    this.Infant = 0
                  }
                  this.infantTotal = (this.Infant * this.infant_price)
                  this.subTotal = (this.adultTotal + this.childTotal + this.infantTotal)
                  localStorage.setItem("subTotal", this.subTotal)
             },
              },
              
           
     })
app.mount("#canvas")


const appBooking = Vue.createApp({
         data() {
             return {
               Adult:  localStorage.getItem("Adult"),
               Children: localStorage.getItem("Children"),
               Infant : localStorage.getItem("Infant"),
               adultTotal  :  localStorage.getItem("adultTotal"),
               childTotal  :  localStorage.getItem("childTotal"),
               subTotal: localStorage.getItem("subTotal")
             
             }
           }, 
          
     })
     appBooking.mount("#personData")

