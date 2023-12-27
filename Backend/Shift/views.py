from rest_framework import viewsets
from .models import GuardRound
from .serializers import GuardRoundSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime, timedelta
from User.models import User
from Shift.models import Shift



class GuardRoundViewSet(viewsets.ModelViewSet):
    queryset = GuardRound.objects.all()
    serializer_class = GuardRoundSerializer

class OrganizeShifts(APIView):
    def put(self, request):

        global lieutenant_arr, soldier_arr, first_lieutenant, first_soldier
        lieutenant_arr = []
        soldier_arr = []
        first_lieutenant = 0
        first_soldier = 0
        
        # Calculate the start and end dates for the next month
        today = datetime.today()
        next_month_start = datetime(today.year, today.month + 1, 1)
        next_month_end = datetime(today.year, today.month + 2, 1) - timedelta(days=1)

        eligible_lieutenants = User.objects.filter(lieutenant=True)
        eligible_soldiers = User.objects.filter(lieutenant=False)

        guard_rounds_for_month = []
        current_date = next_month_start
        while current_date <= next_month_end:
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
                current_lieutenant = 0
                manning_lieutenants = []
        
                while True:
                    if len(manning_lieutenants) == 2:
                        manning_shift = Shift.objects.create(
                            first_guard= manning_lieutenants[0],
                            second_guard= manning_lieutenants[1],
                            shift_type='MANNING_POST'
                        )
                        manning_shift.save()
                        lieutenant_arr.pop(lieutenant_arr[0])
                        lieutenant_arr.pop(lieutenant_arr[1])
                        break

                    if current_lieutenant.off_weekend != current_date.strftime("%d-%m-%Y"):
                        manning_lieutenants.append(current_lieutenant)
                    else:
                        manning_lieutenants.append(current_lieutenant)

                    if current_lieutenant < len(lieutenant_arr):
                        lieutenant_arr.append(eligible_lieutenants[first_lieutenant])
                        first_lieutenant += 1
                    
                    
                    current_soldier = 0
                    manning_A = []    
                    manning_B = []
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
                            soldier_arr.pop(soldier_arr[0])
                            soldier_arr.pop(soldier_arr[1])
                            soldier_arr.pop(soldier_arr[0])
                            soldier_arr.pop(soldier_arr[0])
                            break
                            

                        if current_soldier.off_weekend != current_date.strftime("%d-%m-%Y") and current_soldier.month_frequency == 4:
                            if len(manning_B) < 2 and current_soldier.b_objection == False:
                                manning_B.append(current_soldier)
                            elif len(manning_A) < 2:
                                manning_A.append(current_soldier)

                        if current_soldier < len(soldier_arr):
                            soldier_arr.append(eligible_soldiers[first_soldier])
                            first_soldier += 1
                current_date += timedelta(days=2)

        else:
            current_lieutenant = 0
            manning_lieutenants = []
        
            while True:
                if len(manning_lieutenants) == 2:
                    manning_shift = Shift.objects.create(
                        first_guard= manning_lieutenants[0],
                        second_guard= manning_lieutenants[1],
                        shift_type='MANNING_POST'
                    )
                    manning_shift.save()
                    lieutenant_arr.pop(lieutenant_arr[0])
                    lieutenant_arr.pop(lieutenant_arr[1])
                    break

                if current_lieutenant.off_day1 != current_date.strftime("%d-%m-%Y") and current_lieutenant.off_day2 != current_date.strftime("%d-%m-%Y"):
                    manning_lieutenants.append(current_lieutenant)
                else:
                    manning_lieutenants.append(current_lieutenant)

                if current_lieutenant < len(lieutenant_arr):
                    lieutenant_arr.append(eligible_lieutenants[first_lieutenant])
                    first_lieutenant += 1
                
                
                current_soldier = 0
                manning_A = []    
                manning_B = []
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
                        soldier_arr.pop(soldier_arr[0])
                        soldier_arr.pop(soldier_arr[1])
                        soldier_arr.pop(soldier_arr[0])
                        soldier_arr.pop(soldier_arr[0])
                        break
                        

                    if current_soldier.off_day1 != current_date.strftime("%d-%m-%Y") and current_soldier.off_day2 != current_date.strftime("%d-%m-%Y") and current_soldier.month_frequency == 4:
                        if len(manning_B) < 2 and current_soldier.b_objection == False:
                            manning_B.append(current_soldier)
                        elif len(manning_A) < 2:
                            manning_A.append(current_soldier)

                    if current_soldier < len(soldier_arr):
                        soldier_arr.append(eligible_soldiers[first_soldier])
                        first_soldier += 1


        guard_round = GuardRound.objects.create(
                        start_date= current_date, 
                        end_date= current_date + timedelta(days=1),
                        a_post = a_shift,
                        b_post = b_shift,
                        manning_post = manning_shift
                        )
        guard_round.save()
        guard_rounds_for_month.append(guard_round)
            
        # Move to the next day
        current_date += timedelta(days=1)

        # Update first_lieutenant and first_soldier for the next time
        first_lieutenant = 0 if first_lieutenant >= len(eligible_lieutenants) else first_lieutenant
        first_soldier = 0 if first_soldier >= len(eligible_soldiers) else first_soldier

        # Return the list of GuardRound objects for the month
        return guard_rounds_for_month
    