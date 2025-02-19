import Bloco
from Bloco import FileSystem

fs = FileSystem(20)  # Creates a file system with 20 blocks

# Contiguous allocation
fs.allocate_contiguous("file1.txt", 3)

# Linked allocation
fs.allocate_linked("file2.txt", 4)

# Indexed allocation
fs.allocate_indexed("file3.txt", 3)

fs.display_disk_state()

fs.delete_file("file1.txt")

# Create a file system with 20 blocks
fs = FileSystem(20)

# Display initial state
print("Initial state:")
fs.display_disk_state()

# Test contiguous allocation
print("\nAllocating file1.txt (contiguous, 3 blocks):")
success, message = fs.allocate_contiguous("file1.txt", 3)
print(message)
fs.display_disk_state()

# Test linked allocation
print("\nAllocating file2.txt (linked, 4 blocks):")
success, message = fs.allocate_linked("file2.txt", 4)
print(message)
fs.display_disk_state()

# Test indexed allocation
print("\nAllocating file3.txt (indexed, 3 blocks):")
success, message = fs.allocate_indexed("file3.txt", 3)
print(message)
fs.display_disk_state()

# Test file deletion
print("\nDeleting file1.txt:")
success, message = fs.delete_file("file1.txt")
print(message)
fs.display_disk_state()