<template>
    <div class="max-w-lg mx-auto mt-10 p-6 bg-white shadow-md rounded-lg">
      <h1 class="text-2xl font-bold mb-4">Uploader des fichiers</h1>
  
      <!-- Formulaire d'upload -->
      <form @submit.prevent="uploadFiles" class="space-y-4">
        <input 
          type="file" 
          multiple 
          @change="handleFiles" 
          class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50"
        />
  
        <button 
          type="submit" 
          :disabled="isUploading"
          class="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
        >
          {{ isUploading ? "Envoi en cours..." : "Envoyer" }}
        </button>
      </form>
  
      <!-- Affichage des messages -->
      <p v-if="successMessage" class="text-green-600 mt-3">{{ successMessage }}</p>
      <p v-if="errorMessage" class="text-red-600 mt-3">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script setup lang="ts">
    import { ref } from 'vue'
    import axios from 'axios'
  
    // Déclaration des variables réactives
    const selectedFiles = ref<File[]>([]);
    const isUploading = ref(false)
    const successMessage = ref("")
    const errorMessage = ref("")
  
    // Capture les fichiers sélectionnés
    const handleFiles = (event : Event) => {
      const input = event.target as HTMLInputElement;
      if (input.files) {
        selectedFiles.value = Array.from(input.files);
      }
    };
  
    // Envoie les fichiers au serveur
    const uploadFiles = async () => {
      if (selectedFiles.value.length === 0) {
        errorMessage.value = "Veuillez sélectionner des fichiers."
        return;
      }
  
      isUploading.value = true
      successMessage.value = ""
      errorMessage.value = ""
  
      const formData = new FormData();
      selectedFiles.value.forEach((file) => {
        formData.append(`file[]`, file);  // Utilisation de `file[]` pour chaque fichier
      });
  
      try {
        const response = await axios.post("http://localhost:9000/upload/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
  
        successMessage.value = response.data.message || "Fichiers envoyés avec succès !"
      } catch (error) {
        errorMessage.value = "Fichier(s) uploadés avec succès"
      } finally {
        isUploading.value = false
      }
    };
  </script>
  