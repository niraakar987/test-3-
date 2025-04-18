# Global counter used to generate unique requisition IDs.
# NOTE (SRP improvement): It would be better to encapsulate this inside the class to avoid global state.
counter = 10000

class RequisitionSystem:
    def __init__(self):
        # Requisition list and counters for status tracking.
        # Follows SRP by keeping initialization responsibilities only here.
        self.requisitions = [] 
        self.approved_count = 0
        self.pending_count = 0
        self.not_approved_count = 0

    def staff_info(self):
        """
        Collects staff details and generates a unique requisition ID.
        
        KISS: Only collects essential information (date, ID, name).
        SRP: Slight violation — mixes input collection and ID generation.
        Could be split into two separate methods for clarity and reuse.
        """
        global counter
        date = input("Enter the date (MM/DD/YYYY): ")
        staff_id = input("Enter the Staff ID: ")
        staff_name = input("Enter the Staff Name: ")

        requisition_id = counter + 1
        counter += 1

        return date, staff_id, staff_name, requisition_id

    def get_requisition_items(self):
        """
        Collects multiple item names and prices from the user.

        SRP: Handles item entry only.
        KISS: Simple loop logic using 'done' to end input.
        DRY: Avoids duplication by using a loop.
        """
        items = []
        while True:
            item_name = input("Enter the item name (or type 'done' to finish): ")
            if item_name.lower() == 'done':
                if not items:
                    print("No items entered. Please add items or type 'done'.")
                    continue
                break
            try:
                item_price = float(input(f"Enter the price of {item_name}: $"))
                items.append((item_name, item_price))
            except ValueError:
                print("Invalid price. Please enter a valid number.")
        return items

    def requisitions_total(self):
        """
        Handles full requisition data collection and computes total cost.

        SRP: Combines input logic and total calculation — could be refactored into smaller methods.
        DRY: Uses built-in sum() and method reuse.
        KISS: Uses basic Python structures for clear output.
        """
        date, staff_id, staff_name, requisition_id = self.staff_info()
        items = self.get_requisition_items()
        total_value = sum(item[1] for item in items)  # DRY

        print("\nItems ordered:")
        for item, price in items:
            print(f"{item}: ${price:.2f}")

        return total_value, staff_id, requisition_id, date, staff_name

    def requisition_approval(self, total_value, staff_id, requisition_id):
        """
        Determines if a requisition is approved based on its value.

        SRP: Focused on a single decision.
        KISS: Approval rule is simple (value < 500).
        """
        status = "Pending"
        approval_reference = ""
        if total_value < 500:
            status = "Approved"
            approval_reference = f"{staff_id}{str(requisition_id)[-3:]}"  # DRY: consistent approval format
        return status, approval_reference

    def respond_requisition(self, requisition_id, approval_status):
        """
        Allows manager to manually respond to requisition approval.

        SRP: Handles both updating requisition and adjusting counters — could be separated.
        DRY: Approval reference format is reused.
        """
        for requisition in self.requisitions:
            if requisition['requisition_id'] == requisition_id:
                if approval_status == "Approved":
                    requisition['status'] = "Approved"
                    requisition['approval_reference'] = f"{requisition['staff_id']}{str(requisition['requisition_id'])[-3:]}"
                    self.approved_count += 1
                    self.pending_count -= 1
                elif approval_status == "Not approved":
                    requisition['status'] = "Not approved"
                    requisition['approval_reference'] = "Not available"
                    self.not_approved_count += 1
                    self.pending_count -= 1
                break

    def display_requisitions(self):
        """
        Displays all requisition records.

        SRP: Only handles displaying data.
        KISS: Uses straightforward formatting for easy reading.
        """
        for requisition in self.requisitions:
            print(f"\nDate: {requisition['date']}")
            print(f"Requisition ID: {requisition['requisition_id']}")
            print(f"Staff ID: {requisition['staff_id']}")
            print(f"Staff Name: {requisition['staff_name']}")
            print(f"Total: ${requisition['total_value']:.2f}")
            print(f"Status: {requisition['status']}")
            print("Approval Reference Number:",
                  requisition['approval_reference'] if requisition['status'] == "Approved" else "Not available")

    def requisition_statistics(self):
        """
        Displays the count of each requisition status type.

        SRP: Focused on showing statistics only.
        KISS: Straightforward output logic.
        """
        print("\nDisplaying the Requisition Statistics")
        print(f"The total number of requisitions submitted: {len(self.requisitions)}")
        print(f"The total number of approved requisitions: {self.approved_count}")
        print(f"The total number of pending requisitions: {self.pending_count}")
        print(f"The total number of not approved requisitions: {self.not_approved_count}")

    def create_requisition(self):
        """
        Creates and stores a full requisition object.

        SRP: Mixes multiple actions (gathering data, approving, storing).
        DRY: Makes good use of helper functions to prevent repetition.
        """
        total_value, staff_id, requisition_id, date, staff_name = self.requisitions_total()
        status, approval_reference = self.requisition_approval(total_value, staff_id, requisition_id)

        requisition = {
            'date': date,
            'staff_id': staff_id,
            'staff_name': staff_name,
            'requisition_id': requisition_id,
            'total_value': total_value,
            'status': status,
            'approval_reference': approval_reference
        }

        self.requisitions.append(requisition)

        if status == "Approved":
            self.approved_count += 1
        else:
            self.pending_count += 1

    def main(self):
        """
        Main program loop.

        SRP: Combines user input, control flow, and some validation.
        KISS: Clearly organized menu makes it simple for users.
        """
        while True:
            action = input("\nChoose an action:\n1. Create Requisition\n2. Display Requisitions\n3. Respond to Requisition\n4. View Statistics\n5. Exit\n> ")

            if action == '1':
                self.create_requisition()
            elif action == '2':
                self.display_requisitions()
            elif action == '3':
                try:
                    requisition_id = int(input("Enter the Requisition ID to respond to: "))
                    approval_status = input("Enter the approval status (Approved/Not approved): ").capitalize()
                    if approval_status in ["Approved", "Not approved"]:
                        self.respond_requisition(requisition_id, approval_status)
                    else:
                        print("Invalid status. Please enter 'Approved' or 'Not approved'.")
                except ValueError:
                    print("Invalid input. Requisition ID must be a number.")
            elif action == '4':
                self.requisition_statistics()
            elif action == '5':
                print("Exiting program...")
                break
            else:
                print("Invalid action. Please try again.")

# Entry point for the system
if __name__ == "__main__":
    requisition_system = RequisitionSystem()
    requisition_system.main()
