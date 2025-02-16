import {
  Avatar,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
  NavbarItem,
} from "@nextui-org/react";
import React, { useCallback } from "react";
import { DarkModeSwitch } from "./darkmodeswitch";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";

export const UserDropdown = () => {
  const router = useRouter();
  // Instead of using SWR to fetch user info, we use our AuthContext.
  const { user } = useAuth();

  const handleLogout = useCallback(async () => {
    // Call your FastAPI logout endpoint which deletes the session cookie.
    // Using a relative URL because everything is on the same domain now.
    await fetch(`/api/auth/logout`, {
      method: "POST",
      credentials: "include",
    });
    // Then redirect to the login page; middleware will handle redirection as needed.
    window.location.href = `/login`;
  }, []);

  // Fallback display if user is not loaded yet.
  const displayUser = user || { username: "User", email: "" };

  return (
    <Dropdown>
      <NavbarItem>
        <DropdownTrigger>
          <Avatar
            as="button"
            color="secondary"
            size="md"
            src="https://i.pravatar.cc/150?u=a042581f4e29026704d"
          />
        </DropdownTrigger>
      </NavbarItem>
      <DropdownMenu aria-label="User menu actions">
        <DropdownItem
          key="profile"
          className="flex flex-col justify-start w-full items-start"
        >
          <p>Signed in as</p>
          <p>{displayUser.username}</p>
        </DropdownItem>
        <DropdownItem key="settings">My Settings</DropdownItem>
        <DropdownItem key="team_settings">Team Settings</DropdownItem>
        <DropdownItem key="analytics">Analytics</DropdownItem>
        <DropdownItem key="system">System</DropdownItem>
        <DropdownItem key="configurations">Configurations</DropdownItem>
        <DropdownItem key="help_and_feedback">
          Help &amp; Feedback
        </DropdownItem>
        <DropdownItem
          key="logout"
          color="danger"
          className="text-danger"
          onPress={handleLogout}
        >
          Log Out
        </DropdownItem>
        <DropdownItem key="switch">
          <DarkModeSwitch />
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  );
};
