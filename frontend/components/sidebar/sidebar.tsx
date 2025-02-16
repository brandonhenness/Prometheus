import React from "react";
import { Sidebar } from "./sidebar.styles";
import { Avatar, Tooltip } from "@nextui-org/react";
import { CollegesDropdown } from "./colleges-dropdown";
import { PrometheusLogo } from "../logos/prometheus-logo";

// Dashboard & Core Icons
import { HomeIcon } from "../icons/sidebar/home-icon";
import { SettingsIcon } from "../icons/sidebar/settings-icon";
import { ChangeLogIcon } from "../icons/sidebar/changelog-icon";

// New feature icons (placeholders)
import { EducationIcon } from "../icons/sidebar/education-icon";
import { DegreeIcon } from "../icons/sidebar/degree-icon";
import { ScheduleIcon } from "../icons/sidebar/schedule-icon";
import { TranscriptIcon } from "../icons/sidebar/transcript-icon";
import { PlannerIcon } from "../icons/sidebar/planner-icon";
import { LabIcon } from "../icons/sidebar/lab-icon";
import { OfficeHoursIcon } from "../icons/sidebar/officehours-icon";
import { AssetIcon } from "../icons/sidebar/asset-icon";
import { ReentryIcon } from "../icons/sidebar/reentry-icon";
import { CommunityIcon } from "../icons/sidebar/community-icon";

import { SidebarItem } from "./sidebar-item";
import { SidebarMenu } from "./sidebar-menu";
import { useSidebarContext } from "../layout/layout-context";
import { usePathname } from "next/navigation";

export const SidebarWrapper = () => {
  const pathname = usePathname();
  const { collapsed, setCollapsed } = useSidebarContext();

  return (
    <aside className="h-screen z-[20] sticky top-0">
      {collapsed ? (
        <div className={Sidebar.Overlay()} onClick={setCollapsed} />
      ) : null}
      <div className={Sidebar({ collapsed })}>
        <div className={`${Sidebar.Header()} mb-4`}>
          {/* Prometheus Logo */}
          <PrometheusLogo />
        </div>
        <div className={Sidebar.Header()}>
          {/* College Dropdown below the logo */}
          <CollegesDropdown />
        </div>
        <div className="flex flex-col justify-between h-full">
          <div className={Sidebar.Body()}>
            {/* Dashboard */}
            <SidebarItem
              title="Dashboard"
              icon={<HomeIcon />}
              isActive={pathname === "/"}
              href="/"
            />

            {/* Education Section */}
            <SidebarMenu title="Education">
              <SidebarItem
                title="Learning Materials"
                icon={<EducationIcon />}
                isActive={pathname === "/learning-materials"}
                href="/learning-materials"
              />
              <SidebarItem
                title="Degree Plans"
                icon={<DegreeIcon />}
                isActive={pathname === "/degree-plans"}
                href="/degree-plans"
              />
              <SidebarItem
                title="Course Schedule"
                icon={<ScheduleIcon />}
                isActive={pathname === "/course-schedule"}
                href="/course-schedule"
              />
              <SidebarItem
                title="Transcripts"
                icon={<TranscriptIcon />}
                isActive={pathname === "/transcripts"}
                href="/transcripts"
              />
              <SidebarItem
                title="Study Planner"
                icon={<PlannerIcon />}
                isActive={pathname === "/study-planner"}
                href="/study-planner"
              />
            </SidebarMenu>

            {/* Scheduling Section */}
            <SidebarMenu title="Scheduling">
              <SidebarItem
                title="Computer Lab"
                icon={<LabIcon />}
                isActive={pathname === "/lab-scheduling"}
                href="/lab-scheduling"
              />
              <SidebarItem
                title="Office Hours"
                icon={<OfficeHoursIcon />}
                isActive={pathname === "/office-hours"}
                href="/office-hours"
              />
            </SidebarMenu>

            {/* Staff Tools Section */}
            <SidebarMenu title="Staff Tools">
              <SidebarItem
                title="Asset Management"
                icon={<AssetIcon />}
                isActive={pathname === "/asset-management"}
                href="/asset-management"
              />
            </SidebarMenu>

            {/* Reentry Section */}
            <SidebarMenu title="Reentry">
              <SidebarItem
                title="Reentry Resources"
                icon={<ReentryIcon />}
                isActive={pathname === "/reentry-resources"}
                href="/reentry-resources"
              />
              <SidebarItem
                title="Career Pathways"
                icon={<ReentryIcon />}
                isActive={pathname === "/career-pathways"}
                href="/career-pathways"
              />
            </SidebarMenu>

            {/* Community Section */}
            <SidebarMenu title="Community">
              <SidebarItem
                title="News & Blogs"
                icon={<CommunityIcon />}
                isActive={pathname === "/community"}
                href="/community"
              />
            </SidebarMenu>

            {/* Settings & Updates */}
            <SidebarMenu title="Settings">
              <SidebarItem
                title="App Settings"
                icon={<SettingsIcon />}
                isActive={pathname === "/settings"}
                href="/settings"
              />
              <SidebarItem
                title="Changelog"
                icon={<ChangeLogIcon />}
                isActive={pathname === "/changelog"}
                href="/changelog"
              />
            </SidebarMenu>
          </div>
          <div className={Sidebar.Footer()}>
            <Tooltip content="Settings" color="primary">
              <div className="max-w-fit">
                <SettingsIcon />
              </div>
            </Tooltip>
            <Tooltip content="Profile" color="primary">
              <Avatar
                src="https://i.pravatar.cc/150?u=a042581f4e29026704d"
                size="sm"
              />
            </Tooltip>
          </div>
        </div>
      </div>
    </aside>
  );
};
