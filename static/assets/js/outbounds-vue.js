const inquiryFormOutbound = Vue.createApp({
        
  data() {
    return {
      form: {
        fullname: '',
        email: '',
        mobile: '',
        message: '',
      }
    }
  },
  methods: {
    async submitForm() {
      try {
        const response = await axios.post('/api/inquiry/', this.form)
        console.log(response.data)
      } catch (error) {
        console.error(error)
      }
    }
  }
           
     })
inquiryFormOutbound.mount("#inquiryForm")

