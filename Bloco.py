class Bloco:
    def __init__(self):
        self.is_occupied = False
        self.file_name = None
        self.next_block = None  # For linked allocation
        self.data = None

class FileSystem:
    def __init__(self, total_blocks):
        self.total_blocks = total_blocks
        self.blocks = [Bloco() for _ in range(total_blocks)]
        self.file_table = {}  # Stores file metadata
        self.index_blocks = {}  # For indexed allocation

    def find_contiguous_blocks(self, size):
        """Find a sequence of contiguous free blocks."""
        count = 0
        start_block = -1
        
        for i in range(self.total_blocks):
            if not self.blocks[i].is_occupied:
                if count == 0:
                    start_block = i
                count += 1
                if count == size:
                    return start_block
            else:
                count = 0
        return -1

    def allocate_contiguous(self, file_name, size):
        """Implement contiguous allocation."""
        start_block = self.find_contiguous_blocks(size)
        if start_block == -1:
            return False, "Not enough contiguous space"

        for i in range(start_block, start_block + size):
            self.blocks[i].is_occupied = True
            self.blocks[i].file_name = file_name

        self.file_table[file_name] = {
            'start_block': start_block,
            'size': size,
            'type': 'contiguous'
        }
        return True, f"File allocated from block {start_block} to {start_block + size - 1}"

    def allocate_linked(self, file_name, size):
        """Implement linked allocation."""
        free_blocks = []
        for i in range(self.total_blocks):
            if not self.blocks[i].is_occupied:
                free_blocks.append(i)
                if len(free_blocks) == size:
                    break

        if len(free_blocks) < size:
            return False, "Not enough free blocks"

        # Link the blocks
        for i in range(len(free_blocks)):
            current_block = free_blocks[i]
            self.blocks[current_block].is_occupied = True
            self.blocks[current_block].file_name = file_name
            if i < len(free_blocks) - 1:
                self.blocks[current_block].next_block = free_blocks[i + 1]

        self.file_table[file_name] = {
            'start_block': free_blocks[0],
            'size': size,
            'type': 'linked'
        }
        return True, f"File allocated using linked allocation. Start block: {free_blocks[0]}"

    def allocate_indexed(self, file_name, size):
        """Implement indexed allocation."""
        # First, find an index block
        index_block = -1
        for i in range(self.total_blocks):
            if not self.blocks[i].is_occupied:
                index_block = i
                break

        if index_block == -1:
            return False, "No space for index block"

        # Find data blocks
        data_blocks = []
        for i in range(self.total_blocks):
            if not self.blocks[i].is_occupied and i != index_block:
                data_blocks.append(i)
                if len(data_blocks) == size:
                    break

        if len(data_blocks) < size:
            return False, "Not enough free blocks"

        # Allocate index block and data blocks
        self.blocks[index_block].is_occupied = True
        self.blocks[index_block].file_name = file_name
        self.index_blocks[file_name] = data_blocks

        for block_num in data_blocks:
            self.blocks[block_num].is_occupied = True
            self.blocks[block_num].file_name = file_name

        self.file_table[file_name] = {
            'index_block': index_block,
            'size': size,
            'type': 'indexed'
        }
        return True, f"File allocated using indexed allocation. Index block: {index_block}"

    def delete_file(self, file_name):
        """Delete a file and free its blocks."""
        if file_name not in self.file_table:
            return False, "File not found"

        file_info = self.file_table[file_name]
        
        if file_info['type'] == 'contiguous':
            start = file_info['start_block']
            size = file_info['size']
            for i in range(start, start + size):
                self.blocks[i].is_occupied = False
                self.blocks[i].file_name = None
        
        elif file_info['type'] == 'linked':
            current = file_info['start_block']
            while current is not None:
                next_block = self.blocks[current].next_block
                self.blocks[current].is_occupied = False
                self.blocks[current].file_name = None
                self.blocks[current].next_block = None
                current = next_block
        
        elif file_info['type'] == 'indexed':
            # Free index block
            index_block = file_info['index_block']
            self.blocks[index_block].is_occupied = False
            self.blocks[index_block].file_name = None
            
            # Free data blocks
            for block_num in self.index_blocks[file_name]:
                self.blocks[block_num].is_occupied = False
                self.blocks[block_num].file_name = None
            
            del self.index_blocks[file_name]

        del self.file_table[file_name]
        return True, f"File {file_name} deleted successfully"

    def display_disk_state(self):
        """Display the current state of the disk."""
        print("\nDisk State:")
        print("-" * 50)
        for i in range(self.total_blocks):
            block = self.blocks[i]
            status = f"Block {i:3d}: "
            if block.is_occupied:
                status += f"[Occupied - {block.file_name}]"
                if block.next_block is not None:
                    status += f" -> {block.next_block}"
            else:
                status += "[Free]"
            print(status)
        print("-" * 50)
        print("\nFile Table:")
        for file_name, info in self.file_table.items():
            print(f"{file_name}: {info}")
        print("-" * 50)