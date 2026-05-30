<template>
  <div class="min-h-screen flex flex-col bg-gray-100">
    <header class="bg-slate-800 text-white p-4 shadow-md">
      <h1 class="text-2xl font-bold text-center">ChessTutor</h1>
    </header>

    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar: Game List -->
      <aside class="w-80 bg-white border-r border-gray-300 overflow-y-auto p-4 shadow-inner">
        <h2 class="text-lg font-semibold mb-4 border-b pb-2">Available Games</h2>
        <ul class="space-y-2">
          <li v-for="game in games" :key="game" 
              @click="loadGame(game)"
              class="p-2 rounded cursor-pointer hover:bg-blue-50 transition-colors border border-transparent hover:border-blue-200 text-sm"
              :class="{ 'bg-blue-100 border-blue-300 font-medium': selectedGame === game }">
            <span class="truncate block">{{ game }}</span>
          </li>
        </ul>
        <div v-if="games.length === 0" class="text-gray-500 italic text-sm">
          No games found in data directory.
        </div>
      </aside>

      <!-- Main Content: Chess Board & Analysis -->
      <main class="flex-1 relative flex flex-col items-center justify-center p-4 overflow-auto">
        <div v-if="selectedGame" class="w-full max-w-2xl">
          <div class="mb-4 text-center">
            <h3 class="text-xl font-bold text-slate-700">Analyzing: {{ selectedGame }}</h3>
          </div>
          
<div class="bg-white p-4 rounded-lg shadow-lg">
  <ChessBoard 
    :moves="currentMoves" 
    :selected-move-index="selectedMoveIndex" 
    @move-updated="onMoveReached" 
  />
</div>

          <div class="mt-6 bg-white p-4 rounded-lg shadow text-sm">
            <h4 class="font-bold mb-2 border-b pb-1">Move Notation</h4>
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="(move, index) in currentMoves" 
                :key="index"
                @click="goToMove(index)"
                class="px-2 py-1 bg-gray-200 hover:bg-blue-500 hover:text-white rounded transition-colors"
              >
                {{ move }}
              </button>
            </div>
          </div>
        </div>
        <div v-else class="text-gray-400 text-lg text-center">
          <p>Select a game from the sidebar to begin analysis.</p>
          <p class="text-sm">Make sure the backend is running on port 8000.</p>
        </div>
      </main>
    </div>

    <footer class="bg-slate-800 text-gray-400 text-xs p-2 text-center">
      <p>ChessTutor &copy; 2026 - Professional Chess Analysis</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ChessBoard from './components/ChessBoard.vue'

const games = ref<string[]>([])
const selectedGame = ref<string | null>(null)
const currentMoves = ref<string[]>([])
const selectedMoveIndex = ref<number>(-1)

const fetchGames = async () => {
  try {
    const response = await axios.get('/api/games')
    games.value = response.data
  } catch (error) {
    console.error('Error fetching games:', error)
  }
}

const loadGame = async (game: string) => {
  selectedGame.value = game
  selectedMoveIndex.value = -1
  try {
    const response = await axios.get(`/api/games/${game}`)
    currentMoves.value = response.data.moves
  } catch (error) {
    console.error('Error loading game:', error)
  }
}

const onMoveReached = (move: string) => {
  console.log('Reached move:', move)
}

const goToMove = (index: number) => {
  // Find the move in currentMoves and update selectedGame if needed
  // Since we are already in the game, we just need to update the board position
  // But ChessBoard.vue needs to be notified. 
  // We can use a ref for the selected move index.
  selectedMoveIndex.value = index
}

onMounted(() => {
  fetchGames()
})
</script>