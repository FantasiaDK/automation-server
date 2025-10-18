<template>
  <div class="p-3">
    <hr class="mb-4" />
    <h4 class="text-lg font-semibold mb-4">Create Asset</h4>
    <form @submit.prevent="createAsset">
      <!-- Name Field -->
      <div class="mb-4">
        <label for="name" class="label font-semibold">Name</label>
        <input
          type="text"
          id="name"
          v-model="AssetData.name"
          class="input input-bordered w-full"
          required
        />
      </div>

      <div class="mb-4">
        <label for="data" class="label font-semibold">Data (JSON)</label>
        <textarea 
          id="data" 
          class="textarea textarea-lg textarea-bordered w-full h-96" 
          v-model="AssetData.data"
          placeholder="JSON Data">
        </textarea>
      </div>

      <!-- Buttons -->
      <div class="text-right">
        <button type="submit" class="btn btn-primary" :disabled="passwordMismatch">Create</button>
        <button @click="$emit('close')" type="button" class="btn ml-2">Cancel</button>
      </div>
    </form>
  </div>
</template>


<script>
import { AssetsAPI } from "@/services/automationserver";
import { useAlertStore } from "@/stores/alertStore";

const alertStore = useAlertStore();

export default {
  name: "CreateAsset",
  data() {
    return {
      AssetData: {
        name: "",
        data: ""
      }
    };
  },
  methods: {
    async createAsset() {
      try {
        // Convert AssetData.data to JSON if it's a string
        if (typeof this.AssetData.data === "string") {
          try {
            this.AssetData.data = JSON.parse(this.AssetData.data);
          } catch (error) {
            alertStore.addAlert({
              message: "Invalid JSON format in data field",
              type: "error"
            });
            return;
          }
        }
        await AssetsAPI.createAsset(this.AssetData);
        alertStore.addAlert({
          message: "Asset created successfully",
          type: "success"
        });
        this.$emit("created");
        this.$emit("close");
      } catch (error) {
        alertStore.addAlert({
          message: "Failed to create Asset. Error: " + error.message,
          type: "error"
        });
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
/* Add any required styles here */
</style>