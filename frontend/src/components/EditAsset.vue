<template>
  <div class="p-4">
    <hr class="mb-4" />
    <h4 class="text-lg font-semibold mb-4">Edit Asset</h4>
    <form @submit.prevent="updateAsset" class="space-y-4">
      <!-- Name Field -->
      <div>
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
          v-model="jsonAsString"
          placeholder="JSON Data">
        </textarea>
      </div>

      <!-- Action Buttons -->
      <div class="text-right space-x-2">
        <button type="submit" class="btn btn-primary" :disabled="passwordMismatch">Update</button>
        <button type="button" @click="$emit('close')" class="btn">Cancel</button>
      </div>
    </form>
  </div>
</template>


<script>
import { assetsAPI } from "@/services/automationserver";
import { useAlertStore } from "@/stores/alertStore";

const alertStore = useAlertStore();

export default {
  name: "EditAsset",
  props: {
    Asset: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      AssetData: { ...this.Asset },
      jsonAsString: ""
    };
  },
  watch: {
    Asset: {
      handler(newVal) {
        this.jsonAsString = JSON.stringify(newVal.data, null, 2);
      },
      immediate: true
    }
  },
  methods: {
    async updateAsset() {
      try {
        let data = JSON.parse(this.jsonAsString);
        if (data === null) {
          alertStore.addAlert({
            message: "Invalid JSON format in data field",
            type: "error"
          });
          return;
        }

        this.AssetData.data = data;
        await assetsAPI.updateAsset(this.Asset.id, this.AssetData);
        alertStore.addAlert({
          message: "Asset updated successfully",
          type: "success"
        });
        this.$emit("updated");
        this.$emit("close");
      } catch (error) {
        alertStore.addAlert({
          message: "Failed to update Asset. Error: " + error.message,
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