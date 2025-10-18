<template>
  <content-card title="Assets">
    <template v-slot:header-right>
      <div class="join">
        <!-- Search Icon Button (Small) -->
        <button class="join-item btn btn-square btn-sm">
          <font-awesome-icon :icon="['fas', 'search']" />
        </button>

        <!-- Input Field (Small) -->
        <input type="text" v-model="searchTerm" placeholder="Search Assets..."
          class="join-item input input-bordered input-sm w-full max-w-xs" />
      </div>
      <button @click="showCreateForm = true" class="join-item btn btn-primary btn-sm">+ Create</button>
    </template>
    <div v-if="filteredAssets.length > 0">
      <table class="table w-full mb-3">
        <thead>
          <tr>
            <th class="text-center">ID</th>
            <th>Name</th>
            <th>Username</th>
            <th>Data</th>
            <th>&nbsp;</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="Asset in filteredAssets" :key="Asset.id" class="hover:bg-base-300">
            <td class="text-center">{{ Asset.id }}</td>
            <td>{{ Asset.name }}</td>
            <td>{{ Asset.username }}</td>
            <td><json-view :jsonData="Asset.data" /></td>
            <td class="text-right">
              <dropdown-button :label="'Actions'" :items="[
                { text: 'Edit', icon: 'fas fa-pencil-alt', action: 'edit', id: Asset.id },
                { text: 'Delete', icon: 'fas fa-trash-alt', action: 'delete', id: Asset.id }
              ]" @item-clicked="triggerAction" />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="text-center mb-4" v-else>
      <p class="secondary-content font-semibold">No Assets found.</p>
    </div>


    <edit-Asset v-if="selectedAsset" :Asset="selectedAsset" @close="selectedAsset = null"
      @updated="fetchAssets" />
    <create-Asset v-if="showCreateForm" @close="showCreateForm = false" @created="fetchAssets" />
  </content-card>
</template>

<script>
import { AssetsAPI } from "@/services/automationserver";
import EditAsset from "@/components/EditAsset.vue";
import CreateAsset from "@/components/CreateAsset.vue";
import ContentCard from "@/components/ContentCard.vue";
import DropdownButton from "@/components/DropdownButton.vue";
import { useAlertStore } from "../stores/alertStore";
import JsonView from "@/components/JsonView.vue";

const alertStore = useAlertStore();

export default {
  name: "AssetsView",
  components: {
    EditAsset,
    CreateAsset,
    ContentCard,
    DropdownButton,
    JsonView
  },
  data() {
    return {
      Assets: [],
      selectedAsset: null,
      showCreateForm: false,
      searchTerm: ""
    };
  },
  async created() {
    await this.fetchAssets();
  },
  computed: {
    filteredAssets() {
      return this.Assets.filter(Asset => {
        const term = this.searchTerm.toLowerCase();
        return (
          Asset.name.toLowerCase().includes(term) ||
          Asset.username.toLowerCase().includes(term) ||
          Asset.data.toLowerCase().includes(term)
        );
      }).sort((a, b) => a.name.localeCompare(b.name));
    }
  },
  methods: {
    triggerAction(action, item) {
      if (action === "edit") {
        this.editAsset(this.Assets.find(c => c.id === item.id));
      } else if (action === "delete") {
        this.deleteAsset(item.id);
      }
    },
    async fetchAssets() {
      try {
        this.Assets = await AssetsAPI.getAssets();
      } catch (error) {
        console.error(error);
        alertStore.addAlert({ type: "error", message: error });
      }
    },
    editAsset(Asset) {
      this.selectedAsset = Asset;
    },
    async deleteAsset(AssetId) {
      if (confirm("Are you sure you want to delete this Asset?")) {
        try {
          await AssetsAPI.deleteAsset(AssetId);
          alertStore.addAlert({ type: "succes", message: "Asset deleted successfully" });
          this.fetchAssets();
        } catch (error) {
          console.error(error);
          alertStore.addAlert({ type: "error", message: error });
        }
      }
    }
  }
};
</script>

<style scoped>
/* Add any required styles here */
</style>