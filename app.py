import streamlit as st
import asyncio
import websockets
import json
import uuid


class AIConceptAnalysisClient:
    def __init__(self, server_url='ws://localhost:8765'):
        self.server_url = server_url

    async def send_analysis_request(self, response: str, concept: str):
        """
        Send analysis request to WebSocket server
        """
        try:
            async with websockets.connect(self.server_url) as websocket:
                # Prepare request
                request = {
                    'response': response,
                    'concept': concept,
                    'request_id': str(uuid.uuid4())
                }

                # Send request
                await websocket.send(json.dumps(request))

                # Wait for response
                response = await websocket.recv()
                return json.loads(response)

        except websockets.exceptions.ConnectionClosed:
            st.error("WebSocket connection closed")
        except Exception as e:
            st.error(f"Error connecting to server: {e}")


def main():
    st.title("AI Concept Analysis Platform")

    # Concept selection
    concepts = [
        'machine_learning',
        'neural_networks',
        'ai_ethics'
    ]
    selected_concept = st.selectbox(
        "Select AI Concept",
        concepts
    )

    # Response input
    user_response = st.text_area(
        f"Enter your response about {selected_concept}",
        height=200
    )

    if st.button("Analyze Response"):
        if not user_response:
            st.warning("Please enter a response")
            return

        # Run async WebSocket client
        try:
            result = asyncio.run(
                AIConceptAnalysisClient().send_analysis_request(
                    user_response,
                    selected_concept
                )
            )

            # Display results
            if 'error' in result:
                st.error(result['error'])
            else:
                st.subheader("Analysis Results")

                # Score visualization
                st.progress(result['total_score'] / 100)
                st.metric(
                    label="Concept Understanding Score",
                    value=f"{result['total_score']:.2f}%"
                )

                # Feedback
                st.info(result['feedback'])

        except Exception as e:
            st.error(f"Analysis failed: {e}")


if __name__ == "__main__":
    main()