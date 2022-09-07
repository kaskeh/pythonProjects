<template>
  <div class="home">
    <homeHeader />
  </div>
</template>

<script>
// @ is an alias to /src
import homeHeader from "@/components/siteHeaders/headerStyle0.vue";

export default {
  name: "HomeView",
  components: {
    homeHeader,
  },
};
</script>
