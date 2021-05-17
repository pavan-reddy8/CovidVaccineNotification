from cowin_api import CoWinAPI

def get_state_district_info(state_id):
	cowin = CoWinAPI()
	states = cowin.get_states()
	print(states)

	districts = cowin.get_districts(state_id)
	print(districts)
	
get_state_district_info(16)