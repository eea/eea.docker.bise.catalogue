docker exec eeadockerbisecatalogue_web_1 sh -c "rake environment tire:import PARAMS='{:per_page => 10}' CLASS='Article' FORCE=true"
