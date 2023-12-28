from rest_framework import viewsets
from .models import GuardRound
from .serializers import GuardRoundSerializer
from rest_framework.views import APIView
from datetime import datetime, timedelta
from User.models import User
from Shift.models import Shift
from django.http import JsonResponse
from .serializers import GuardRoundSerializer
from .models import GuardRound

class GuardRoundViewSet(viewsets.ModelViewSet):
    queryset = GuardRound.objects.all()
    serializer_class = GuardRoundSerializer


class OrganizeShifts(APIView):
    def get(self, request):

        global lieutenant_arr, soldier_arr, first_lieutenant, first_soldier
        lieutenant_arr = []
        soldier_arr = []
        first_lieutenant = 0
        first_soldier = 0
        
        # Calculate the start and end dates for the next month
        today = datetime.today()
        next_month_start = datetime(today.year + (today.month + 1) // 12, (today.month + 1) % 12 + 1, 1)
        next_month_end = datetime(today.year + (today.month + 2) // 12, (today.month + 2) % 12 + 1, 1) - timedelta(days=1)

        eligible_lieutenants = User.objects.filter(lieutenant=True)
        eligible_soldiers = User.objects.filter(lieutenant=False)

        guard_rounds_for_month = []
        current_date = next_month_start
        while current_date <= next_month_end:
            print(current_date)
            manning_shift = None
            a_shift =  None
            b_shift = None

            #Get round of lieutenants
            while len(lieutenant_arr) < 2:
                    if first_lieutenant < len(eligible_lieutenants):
                        lieutenant_arr.append(eligible_lieutenants[first_lieutenant])
                        first_lieutenant += 1
            #Get round of soldiers
            while len(soldier_arr) < 4:
                if first_soldier < len(eligible_soldiers):
                    soldier_arr.append(eligible_soldiers[first_soldier])
                    first_soldier += 1

            if current_date.weekday() == 3:  # Thursday
                lieutenant_index = 0
                manning_lieutenants = []
        
                while True:
                    if len(manning_lieutenants) == 2:
                        manning_shift = Shift.objects.create(
                            first_guard= manning_lieutenants[0],
                            second_guard= manning_lieutenants[1],
                            shift_type='MANNING_POST'
                        )
                        manning_shift.save()
                        lieutenant_arr.remove(manning_lieutenants[0])
                        lieutenant_arr.remove(manning_lieutenants[1])
                        # reset_month_frequency(manning_lieutenants)
                        break
                    current_lieutenant = lieutenant_arr[lieutenant_index]
                    #Add lieutenant to shift if available
                    if current_lieutenant.off_weekend != current_date.strftime("%d-%m-%Y"):
                        manning_lieutenants.append(current_lieutenant)
                    
                    #In case we reached end of all lieutenants
                    if first_lieutenant >= len(eligible_lieutenants):
                        lieutenant_arr.append(eligible_lieutenants[first_lieutenant])
                        first_lieutenant = 1
                    #If there are no more options, add new
                    if lieutenant_index >= len(lieutenant_arr) - 1:
                            lieutenant_arr.append(eligible_lieutenants[first_lieutenant])
                            lieutenant_index = 0
                            first_lieutenant += 1
                    lieutenant_index += 1
                    
                    manning_A = []    
                    manning_B = []
                    soldier_index = 0
                    while True:
                        #When there are enough people
                        if len(manning_B) == 2 and len(manning_A) == 2:
                            a_shift = Shift.objects.create(
                            first_guard= manning_A[0],
                            second_guard= manning_A[1],
                            shift_type='A'
                            )
                            a_shift.save()
                            b_shift = Shift.objects.create(
                            first_guard= manning_B[0],
                            second_guard= manning_B[1],
                            shift_type='B'
                            )
                            b_shift.save()
                            for soldier in manning_A + manning_B:
                                if soldier in soldier_arr:
                                    soldier_arr.remove(soldier)
                            break
                            # reset_month_frequency(manning_A)
                            # reset_month_frequency(manning_B)
                        current_soldier = soldier_arr[soldier_index]
                        if current_soldier.off_weekend != current_date.strftime("%d-%m-%Y"):
                            if len(manning_B) < 2 and current_soldier.b_objection == False:
                                manning_B.append(current_soldier)
                            elif len(manning_A) < 2:
                                manning_A.append(current_soldier)
                       
                        #In case we reached end of all lieutenants
                        if first_soldier >= len(eligible_soldiers):
                            soldier_arr.append(eligible_soldiers[first_soldier])
                            first_soldier = 1
                        #If there are no more options, add new
                        if soldier_index >= len(soldier_arr) - 1:
                                soldier_arr.append(eligible_soldiers[first_soldier])
                                first_soldier += 1
                        soldier_index += 1

                shift_json ={current_date.day:
                        {"a_post":{
                            "first_guard": str(a_shift.first_guard.first_name +" "+ a_shift.first_guard.last_name),
                            "second_guard": str(a_shift.second_guard.first_name +" "+ a_shift.second_guard.last_name)
                        },
                        "b_post":{
                            "first_guard": str(b_shift.first_guard.first_name +" "+ b_shift.first_guard.last_name),
                            "second_guard": str(b_shift.second_guard.first_name +" "+ b_shift.second_guard.last_name)

                        },
                        "manning_post":{
                            "first_guard": str(manning_shift.first_guard.first_name +" "+ manning_shift.first_guard.last_name),
                            "second_guard": str(manning_shift.second_guard.first_name +" "+ manning_shift.second_guard.last_name)
                        },
                        }
                    }
                guard_rounds_for_month.append(shift_json)
                current_date += timedelta(days=3)
                break

            else:

                lieutenant_index = 0
                manning_lieutenants = []
            
                while True:
                
                    if len(manning_lieutenants) == 2:
                        manning_shift = Shift.objects.create(
                            first_guard= manning_lieutenants[0],
                            second_guard= manning_lieutenants[1],
                            shift_type='MANNING_POST'
                        )
                        manning_shift.save()
                        lieutenant_arr.remove(manning_lieutenants[0])
                        lieutenant_arr.remove(manning_lieutenants[1])
                        # reset_month_frequency(manning_lieutenants)
                        break
                    current_lieutenant = lieutenant_arr[lieutenant_index]
                    #Add lieutenant to shift if available
                    if current_lieutenant.off_day1 != current_date.strftime("%d-%m-%Y") and current_lieutenant.off_day2 != current_date.strftime("%d-%m-%Y"):
                        manning_lieutenants.append(current_lieutenant)
                    
                    #In case we reached end of all lieutenants
                    if first_lieutenant >= len(eligible_lieutenants):
                        lieutenant_arr.append(eligible_lieutenants[first_lieutenant])
                        first_lieutenant = 1
                    #If there are no more options, add new
                    if lieutenant_index >= len(lieutenant_arr) - 1:
                            lieutenant_arr.append(eligible_lieutenants[first_lieutenant])
                            lieutenant_index = 0
                            first_lieutenant += 1
                    lieutenant_index += 1
                    
                    manning_A = []    
                    manning_B = []
                    soldier_index = 0
                    while True:
                        #When there are enough people
                        if len(manning_B) == 2 and len(manning_A) == 2:
                            a_shift = Shift.objects.create(
                            first_guard= manning_A[0],
                            second_guard= manning_A[1],
                            shift_type='A'
                            )
                            a_shift.save()
                            b_shift = Shift.objects.create(
                            first_guard= manning_B[0],
                            second_guard= manning_B[1],
                            shift_type='B'
                            )
                            b_shift.save()
                            for soldier in manning_A + manning_B:
                                if soldier in soldier_arr:
                                    soldier_arr.remove(soldier)
                            break
                            # reset_month_frequency(manning_A)
                            # reset_month_frequency(manning_B)
                        current_soldier = soldier_arr[soldier_index]
                        if current_soldier.off_day1 != current_date.strftime("%d-%m-%Y") and current_soldier.off_day2 != current_date.strftime("%d-%m-%Y"):
                            if len(manning_B) < 2 and current_soldier.b_objection == False:
                                manning_B.append(current_soldier)
                            elif len(manning_A) < 2:
                                manning_A.append(current_soldier)
                        
                        #In case we reached end of all lieutenants
                        if first_soldier >= len(eligible_soldiers):
                            soldier_arr.append(eligible_soldiers[first_soldier])
                            first_soldier = 1
                        #If there are no more options, add new
                        if soldier_index >= len(soldier_arr) - 1:
                                soldier_arr.append(eligible_soldiers[first_soldier])
                                first_soldier += 1
                        soldier_index += 1

                shift_json ={current_date.day:
                        {"a_post":{
                            "first_guard": str(a_shift.first_guard.first_name +" "+ a_shift.first_guard.last_name),
                            "second_guard": str(a_shift.second_guard.first_name +" "+ a_shift.second_guard.last_name)
                        },
                        "b_post":{
                            "first_guard": str(b_shift.first_guard.first_name +" "+ b_shift.first_guard.last_name),
                            "second_guard": str(b_shift.second_guard.first_name +" "+ b_shift.second_guard.last_name)

                        },
                        "manning_post":{
                            "first_guard": str(manning_shift.first_guard.first_name +" "+ manning_shift.first_guard.last_name),
                            "second_guard": str(manning_shift.second_guard.first_name +" "+ manning_shift.second_guard.last_name)
                        },
                        }
                    }
                print(shift_json)
                guard_rounds_for_month.append(shift_json)
            
                # Move to the next day
                current_date += timedelta(days=1)

        # Update first_lieutenant and first_soldier for the next time
        first_lieutenant = 0 if first_lieutenant >= len(eligible_lieutenants) else first_lieutenant
        first_soldier = 0 if first_soldier >= len(eligible_soldiers) else first_soldier

        # Return the list of GuardRound objects for the month
        return JsonResponse(guard_rounds_for_month, safe=False)
    
# def reset_month_frequency(users_arr):
#     for user in users_arr:
#         user.month_frequency = 1
#         user.save()