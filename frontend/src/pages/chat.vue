<template>
    <div class="max-w-lg mx-auto mt-10 p-6 bg-white shadow-md rounded-lg">
      <h1 class="text-2xl font-bold mb-4">Chat Veto Entreprise</h1>
  
      <div class="border p-4 mb-4 h-64 overflow-y-auto bg-gray-100 rounded">
        <div v-for="(msg, index) in messages" :key="index" class="mb-2">
          <span :class="msg.sender === 'user' ? 'text-blue-600' : 'text-green-600'">
            {{ msg.sender }}:
          </span>
          
          {{ msg.text }}
          <br>
        </div>
        
      </div>
  
      <form @submit.prevent="sendMessage" class="flex">
        <input 
          v-model="userMessage"
          type="text" 
          class="flex-1 border p-2 rounded-l" 
          placeholder="Tapez un message..."
        />
        <button 
          type="submit"
          class="bg-blue-500 text-white px-4 py-2 rounded-r hover:bg-blue-600"
          :disabled="isLoading"
        >
          Envoyer
        </button>
      </form>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  
  // Interface pour un message
  interface Message {
    sender: 'user' | 'server';
    text: string;
  }
  
  const userMessage = ref('');
  const messages = ref<Message[]>([]);
  const isLoading = ref(false);
  
  // Fonction pour envoyer un message et lire la réponse en streaming
  const sendMessage = async () => {
    if (!userMessage.value.trim()) return;
  
    messages.value.push({ sender: 'user', text: userMessage.value });
    isLoading.value = true;
  
    const response = await fetch('http://localhost:9000/openai/chat/?prompt=""'+userMessage.value+'"', {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain' },
    });
    isLoading.value = false
  
    userMessage.value = ''; // Réinitialiser l'input
  
    if (!response.body) {
      messages.value.push({ sender: 'server', text: "Erreur: aucune réponse du serveur." });
      isLoading.value = false;
      return;
    }
  
    // Lire la réponse en streaming
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let receivedText = '';
    let serverMessageIndex = messages.value.length;
  
    messages.value.push({ sender: 'server', text: '' }); // Placeholder pour la réponse en cours
  
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
  
      receivedText += decoder.decode(value, { stream: true });
      messages.value[serverMessageIndex].text = receivedText; // Mise à jour en direct
    }
  
    isLoading.value = false;
  };
  </script>
  