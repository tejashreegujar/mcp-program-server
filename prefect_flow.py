from prefect import flow

@flow(name="get-program-details-flow")
def get_program_details_flow(program_id: str):
    # Simulate DB / business logic
    return {
        "programId": program_id,
        "programName": f"Program {program_id}",
        "status": "active",
        "startDate": "2024-01-01",
        "endDate": "2024-12-31"
    }

if __name__ == "__main__":
    get_program_details_flow.serve(name="program-service")