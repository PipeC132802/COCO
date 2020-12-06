<template>

    <div v-if="!authentication.userIsAuthenticated">
        {{authentication}}
        <h1>Welcome</h1>
    </div>
</template>

<script>
import {mapState} from "vuex";
export default {
    name: 'Welcome',
    created(){
        
    },
    computed:{
        ...mapState(["authentication"])
    }
}
</script>