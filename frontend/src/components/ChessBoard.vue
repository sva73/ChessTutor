<template>
  <div class="flex flex-col items-center">
    <div ref="boardElement" class="chess-board shadow-2xl border-4 border-slate-300 rounded-sm" style="width: 400px; height: 400px;"></div>
    
    <div class="mt-4 flex gap-4">
      <button 
        @click="undoMove" 
        :disabled="currentMoveIndex === 0"
        class="px-4 py-2 bg-slate-700 text-white rounded disabled:opacity-50 hover:bg-slate-600 transition-colors"
      >
        &larr; Previous
      </button>
      <button 
        @click="redoMove" 
        :disabled="currentMoveIndex === moves.length - 1"
        class="px-4 py-2 bg-slate-700 text-white rounded disabled:opacity-50 hover:bg-slate-600 transition-colors"
      >
        Next &rarr;
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Chess } from 'chess.js'
import { Chessground } from 'chessground'
import 'chessground/assets/chessground.base.css'
import 'chessground/assets/chessground.cburnett.css'

const props = defineProps<{
  moves: string[]
  selectedMoveIndex?: number
}>()

const emit = defineEmits<{
  (e: 'move-updated', move: string): void
}>()

const boardElement = ref<HTMLElement | null>(null)
const cg = ref<any>(null)
const currentMoveIndex = ref(-1)

const updateBoard = () => {
  const game = new Chess()
  
  // Apply moves up to the current index
  for (let i = 0; i <= currentMoveIndex.value; i++) {
    if (props.moves[i]) {
      try {
        game.move(props.moves[i])
      } catch (e) {
        console.error('Invalid move:', props.moves[i], e)
      }
    }
  }
  
  // Prepare pieces for chessground
  const board = game.board().map(row => 
    row.map(square => {
      if (!square) return { color: 'none', type: 'none' }
      return {
        color: square.color,
        type: square.type
      }
    })
  )

  if (cg.value) {
    cg.value.setPieces(board)
  }
          
  const moveNotation = props.moves[currentMoveIndex.value] || ''
  emit('move-updated', moveNotation)
}

const undoMove = () => {
  if (currentMoveIndex.value >= 0) {
    currentMoveIndex.value--
    updateBoard()
  }
}

const redoMove = () => {
  if (currentMoveIndex.value < props.moves.length - 1) {
    currentMoveIndex.value++
    updateBoard()
  }
}

onMounted(() => {
  if (boardElement.value) {
    cg.value = Chessground(boardElement.value, {
      movable: {
        free: false
      },
      animation: {
        enabled: true,
        duration: 250
      }
    })
  }
})

watch(() => props.moves, (newMoves: string[]) => {
  if (newMoves && newMoves.length > 0) {
    currentMoveIndex.value = 0
    updateBoard()
  }
}, { immediate: true })

watch(() => props.selectedMoveIndex, (newIndex: number | undefined) => {
  if (newIndex !== undefined && newIndex >= 0 && newIndex < props.moves.length) {
    currentMoveIndex.value = newIndex
    updateBoard()
  }
}, { immediate: true })
</script>

<style scoped>
.chess-board {
  user-select: none;
}
</style>