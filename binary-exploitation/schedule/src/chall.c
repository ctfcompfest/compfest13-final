#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<time.h>
#define MAX_SCHEDULE 1000

int menu() {
    puts("\nMenu:");
    puts("1. Create new schedule");
    puts("2. Edit existing schedule");
    puts("3. Delete schedule");
    puts("4. View schedule");
    puts("5. Add favorite");
    puts("6. Edit favorite");
    puts("7. Exit");
    printf("> ");
    

    int choice;
	scanf("%d", &choice);
	return choice;
}

void greetings() {
    puts("Take notes of your schedule with our app!");
}

struct Schedule {
    char *description;
    time_t startTime;
    time_t endTime;
};

struct Schedule *schedule[MAX_SCHEDULE];
int scheduleCnt = 0;
int isDeleted[MAX_SCHEDULE];

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    memset(isDeleted, 0, sizeof(isDeleted));
}

void removeDeletedScheduleFromArray() {
    for (int i = 0; i < scheduleCnt; i++) {
        if (isDeleted[i] == 1) {
            isDeleted[i] = 0;
            for (int j = i; j < scheduleCnt - 1; j++) {
                int tmp = isDeleted[j];
                isDeleted[j] = isDeleted[j + 1];
                isDeleted[j + 1] = tmp;

                struct Schedule *tmpSchedule = schedule[j];
                schedule[j] = schedule[j + 1];
                schedule[j + 1] = tmpSchedule;
            }
            scheduleCnt--;
        }
    }
}

void createSchedule() {
    removeDeletedScheduleFromArray();
    if (scheduleCnt == MAX_SCHEDULE) {
        puts("You have reach the limit for now.");
        return;
    }

    char tmpDescription[2005];
    puts("Describe your schedule in detail.");
    printf("> ");
    scanf("%2000s", tmpDescription);
    char *description = malloc(strlen(tmpDescription));
    strncpy(description, tmpDescription, strlen(tmpDescription));

    puts("When is the start time?");
    struct tm t_start_time;
    t_start_time.tm_isdst = -1;
    printf("> Day: ");
    scanf("%d", &(t_start_time.tm_mday));
    printf("> Month: ");
    scanf("%d", &(t_start_time.tm_mon));
    t_start_time.tm_mon--;
    printf("> Year: ");
    scanf("%d", &(t_start_time.tm_year));
    t_start_time.tm_year -= 1900;
    printf("> Hour: ");
    scanf("%d", &(t_start_time.tm_hour));
    printf("> Minute: ");
    scanf("%d", &(t_start_time.tm_min));
    printf("> Second: ");
    scanf("%d", &(t_start_time.tm_sec));

    puts("When is the end time?");
    struct tm t_end_time;
    t_end_time.tm_isdst = -1;
    printf("> Day: ");
    scanf("%d", &(t_end_time.tm_mday));
    printf("> Month: ");
    scanf("%d", &(t_end_time.tm_mon));
    t_end_time.tm_mon--;
    printf("> Year: ");
    scanf("%d", &(t_end_time.tm_year));
    t_end_time.tm_year -= 1900;
    printf("> Hour: ");
    scanf("%d", &(t_end_time.tm_hour));
    printf("> Minute: ");
    scanf("%d", &(t_end_time.tm_min));
    printf("> Second: ");
    scanf("%d", &(t_end_time.tm_sec));

    schedule[scheduleCnt] = malloc(sizeof(struct Schedule));
    schedule[scheduleCnt]->description = description;
    schedule[scheduleCnt]->startTime = mktime(&t_start_time);
    schedule[scheduleCnt]->endTime = mktime(&t_end_time);

    scheduleCnt++;

    puts("Schedule created successfully.");
}

void editSchedule() {
    printf("Which schedule do you want to edit?\n> ");
    int choice;
    scanf("%d", &choice);
    if (choice >= scheduleCnt) {
        puts("Schedule not found.");
        return;
    }
    int idx = choice;

    printf("Which one do you want to edit?\n1. Description\n2. Start time\n3. End time\n> ");
    scanf("%d", &choice);
    if (choice == 1) {
        char tmpDescription[2005];
        puts("Describe your schedule in detail.");
        printf("> ");
        scanf("%2000s", tmpDescription);
        char *description = malloc(strlen(tmpDescription));
        strncpy(description, tmpDescription, strlen(tmpDescription));
        schedule[idx]->description = description;
    } else if (choice == 2) {
        puts("When is the start time?");
        struct tm t_start_time;
        t_start_time.tm_isdst = -1;
        printf("> Day: ");
        scanf("%d", &(t_start_time.tm_mday));
        printf("> Month: ");
        scanf("%d", &(t_start_time.tm_mon));
        t_start_time.tm_mon--;
        printf("> Year: ");
        scanf("%d", &(t_start_time.tm_year));
        t_start_time.tm_year -= 1900;
        printf("> Hour: ");
        scanf("%d", &(t_start_time.tm_hour));
        printf("> Minute: ");
        scanf("%d", &(t_start_time.tm_min));
        printf("> Second: ");
        scanf("%d", &(t_start_time.tm_sec));
        schedule[idx]->startTime = mktime(&t_start_time);
    } else if (choice == 3) {
        puts("When is the end time?");
        struct tm t_end_time;
        t_end_time.tm_isdst = -1;
        printf("> Day: ");
        scanf("%d", &(t_end_time.tm_mday));
        printf("> Month: ");
        scanf("%d", &(t_end_time.tm_mon));
        t_end_time.tm_mon--;
        printf("> Year: ");
        scanf("%d", &(t_end_time.tm_year));
        t_end_time.tm_year -= 1900;
        printf("> Hour: ");
        scanf("%d", &(t_end_time.tm_hour));
        printf("> Minute: ");
        scanf("%d", &(t_end_time.tm_min));
        printf("> Second: ");
        scanf("%d", &(t_end_time.tm_sec));
        schedule[idx]->endTime = mktime(&t_end_time);
    }

    puts("Schedule edited successfully.");
}

void deleteSchedule() {
    if (scheduleCnt == 0) {
        puts("You don\'t have any schedule.");
        return;
    }

    puts("Which schedule you want to delete?");
    printf("> ");

    int choice;
    scanf("%d", &choice);

    if (choice >= scheduleCnt || isDeleted[choice] == 1) {
        puts("Schedule not found.");
        return;
    }

    isDeleted[choice] = 1;
    free(schedule[choice]->description);
    puts("Schedule deleted successfully.");
}

char *favorite[MAX_SCHEDULE];
int cntFavorite = 0;
void favoriteSchedule() {
    if (cntFavorite > 0) {
        puts("");
        puts("Favorite(s):");
    }
    for (int i = 0; i < cntFavorite; i++) {
        printf("%d. %s\n", i, favorite[i]);
    }
}

void addFavorite() {
    printf("Which one do you want to add as favorite?\n> ");
    int idx;
    scanf("%d", &idx);
    if (idx >= scheduleCnt) {
        puts("Schedule not found.");
        return;
    }
    printf("Do you want to edit your description first? (0/1): ");
    int choice;
    scanf("%d", &choice);
    if (choice == 1) {
        puts("Describe your schedule in detail.");
        printf("> ");
        scanf("%2000s", schedule[idx]->description);
        favorite[cntFavorite] = schedule[idx]->description;
    } else{
        favorite[cntFavorite] = calloc(strlen(schedule[idx]->description), 1);
        strncpy(favorite[cntFavorite], schedule[idx]->description, strlen(schedule[idx]-> description));
    }
    cntFavorite++;

    puts("Schedule added to favorite list successfully.");
}

void editFavorite() {
    printf("Which one do you want to edit?\n> ");
    int idx;
    scanf("%d", &idx);
    if (idx >= cntFavorite) {
        puts("Schedule not found.");
        return;
    }
    puts("Describe your schedule in detail.");
    printf("> ");
    scanf("%2000s", favorite[idx]);
    puts("Schedule edited successfully.");
}

void viewSchedule() {
    if (scheduleCnt == 0) {
        puts("Currently you don\'t have any schedule.");
        return;
    }
    char buf[80];
    for (int i = 0; i < scheduleCnt; i++) {
        if (isDeleted[i] == 0) {
            printf("%d. %s\n", i, schedule[i]->description);

            struct tm start = *localtime(&schedule[i]->startTime);
            strftime(buf, sizeof(buf), "%a %Y-%m-%d %H:%M:%S %Z", &start);
            printf("Start time: %s\n", buf);

            struct tm end = *localtime(&schedule[i]->endTime);
            strftime(buf, sizeof(buf), "%a %Y-%m-%d %H:%M:%S %Z", &end);
            printf("End time: %s", buf);

            puts("");
        }
    }
}

int main() {
    init();
    greetings();
    while (1) {
        favoriteSchedule();
        int choice = menu();
        if (choice == 1) {
            createSchedule();
        } else if (choice == 2) {
            editSchedule();
        } else if (choice == 3) {
            deleteSchedule();
        } else if (choice == 4) {
            viewSchedule();
        } else if (choice == 5) {
            addFavorite();
        } else if (choice == 6) {
            editFavorite();
        } else if (choice == 7) {
            puts("Bye.");
            exit(0);
        }
    }
}