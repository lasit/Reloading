#!/bin/bash

# Kill any existing Streamlit processes
pkill -f streamlit

# Start the main app
echo "Starting Main App on port 8501..."
streamlit run app.py --server.port 8501 > app.log 2>&1 &
MAIN_PID=$!
echo "Main App started with PID $MAIN_PID"

# Wait a moment before starting the next app
sleep 2

# Start the analysis app
echo "Starting Data Analysis on port 8502..."
streamlit run analysis.py --server.port 8502 > analysis.log 2>&1 &
ANALYSIS_PID=$!
echo "Data Analysis started with PID $ANALYSIS_PID"

# Wait a moment before starting the next app
sleep 2

# Start the admin app
echo "Starting Admin Interface on port 8503..."
streamlit run admin.py --server.port 8503 > admin.log 2>&1 &
ADMIN_PID=$!
echo "Admin Interface started with PID $ADMIN_PID"

echo ""
echo "All applications started successfully!"
echo ""
echo "Access your applications at:"
echo "  • Main App: http://localhost:8501"
echo "  • Data Analysis: http://localhost:8502"
echo "  • Admin Interface: http://localhost:8503"
echo ""
echo "To stop all applications, run: pkill -f streamlit"
echo ""
echo "Log files:"
echo "  • Main App: app.log"
echo "  • Data Analysis: analysis.log"
echo "  • Admin Interface: admin.log"
